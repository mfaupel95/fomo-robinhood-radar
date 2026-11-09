"""Windows owned process trees: atomic job membership at creation -> resume.

No PID enumeration/kill and no taskkill helper. Descendants inherit membership;
no breakaway flag is permitted. The non-inheritable job handle is kill-on-close,
including when the supervisor crashes. Unsupported job-list attributes fail
before CreateProcessW; there is no separate create/assign window.
"""
from __future__ import annotations
import os
import subprocess
import time

# Strong ownership survives a caller discarding an exception after classification.
# Only successful closes remove entries; this is not a PID cleanup service.
_pending_owners = []


class ProcessCleanupError(RuntimeError):
    """The owned process tree could not be safely started or reaped (transient)."""

    def __init__(self, message, *, owner=None, errors=()):
        super().__init__(message)
        self.owner = owner  # Preserve failed-close ownership, including startup.
        self.errors = tuple(errors)


class WindowsTree:
    def __init__(self, args, env, native=None):
        self.native = native if native is not None else _Native()
        self.job = self.process = self.thread = None
        self.pid = None
        try:
            self.job = self.native.create_job()
            self.process, self.thread, self.pid = self.native.spawn_suspended(args, env, self.job)
            self.native.resume(self.thread)
            self.native.close(self.thread)
            self.thread = None
        except BaseException as exc:
            errors = [exc]
            try:
                if self.process is not None:
                    self.native.terminate_process(self.process)
                    self.native.wait_process(self.process, 3)
            except Exception as cleanup_exc:
                errors.append(cleanup_exc)
            self._close_handles(errors)
            self._remember_ownership()
            raise ProcessCleanupError('Windows tree startup failed; cleanup errors retained', owner=self, errors=errors) from exc

    def _remember_ownership(self):
        pending = any(getattr(self, name) is not None for name in ('thread', 'process', 'job'))
        pending = pending or bool(getattr(self.native, 'reap', ())) or bool(getattr(self.native, 'pending_handles', ()))
        if pending and self not in _pending_owners:
            _pending_owners.append(self)
        elif not pending and self in _pending_owners:
            _pending_owners.remove(self)

    def _close_handles(self, errors):
        close_pending = getattr(self.native, 'close_pending', None)
        if close_pending is not None:
            try:
                close_pending()
            except Exception as exc:
                errors.append(exc)
        for name in ('thread', 'process', 'job'):
            handle = getattr(self, name)
            if handle is not None:
                try:
                    self.native.close(handle)
                except Exception as exc:
                    errors.append(exc)
                else:
                    setattr(self, name, None)

    def wait(self, timeout):
        return self.native.wait_process(self.process, timeout)

    def close(self):
        errors = []
        if self.job is not None:
            try:
                self.native.terminate_job(self.job)
                self.native.wait_empty(self.job, 3)
            except Exception as exc:
                errors.append(exc)
        self._close_handles(errors)
        self._remember_ownership()
        if errors:
            raise ProcessCleanupError('Windows job cleanup not confirmed', owner=self, errors=errors) from errors[0]


def windows_bounded(args, env, timeout):
    tree = WindowsTree(args, env)
    try:
        try:
            return tree.wait(timeout)
        except subprocess.TimeoutExpired:
            return 124
    finally:
        tree.close()


class _Native:
    def __init__(self):
        import ctypes as ct
        from ctypes import wintypes as wt
        import _winapi
        self.ct, self.wt, self.api = ct, wt, _winapi
        self.reap = []
        self.pending_handles = []
        self.k = ct.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateJobObjectW': ([ct.c_void_p, wt.LPCWSTR], wt.HANDLE),
            'SetInformationJobObject': ([wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD], wt.BOOL),
            'QueryInformationJobObject': ([wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD, ct.c_void_p], wt.BOOL),

            'TerminateJobObject': ([wt.HANDLE, wt.UINT], wt.BOOL),
            'ResumeThread': ([wt.HANDLE], wt.DWORD),
            'OpenProcess': ([wt.DWORD, wt.BOOL, wt.DWORD], wt.HANDLE),
            'IsProcessInJob': ([wt.HANDLE, wt.HANDLE, ct.POINTER(wt.BOOL)], wt.BOOL),
        }
        for name, (args, result) in signatures.items():
            fn = getattr(self.k, name)
            fn.argtypes, fn.restype = args, result

    def check(self, result):
        if not result:
            raise self.ct.WinError(self.ct.get_last_error())
        return result

    def create_job(self):
        ct, wt = self.ct, self.wt
        class Basic(ct.Structure):
            _fields_ = [('process_time', ct.c_longlong), ('job_time', ct.c_longlong),
                        ('flags', wt.DWORD), ('min_ws', ct.c_size_t), ('max_ws', ct.c_size_t),
                        ('active_limit', wt.DWORD), ('affinity', ct.c_size_t),
                        ('priority', wt.DWORD), ('scheduling', wt.DWORD)]
        class IO(ct.Structure):
            _fields_ = [(name, ct.c_ulonglong) for name in ('read_ops','write_ops','other_ops','read_bytes','write_bytes','other_bytes')]
        class Extended(ct.Structure):
            _fields_ = [('basic', Basic), ('io', IO), ('process_memory', ct.c_size_t),
                        ('job_memory', ct.c_size_t), ('peak_process', ct.c_size_t), ('peak_job', ct.c_size_t)]
        job = self.check(self.k.CreateJobObjectW(None, None))
        try:
            limits = Extended()
            limits.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE only
            self.check(self.k.SetInformationJobObject(job, 9, ct.byref(limits), ct.sizeof(limits)))
            return job
        except BaseException:
            try:
                self.close(job)
            except Exception as exc:
                self.pending_handles.append(job)
                raise ProcessCleanupError('job setup and job close failed', owner=self, errors=[exc]) from exc
            raise

    def spawn_suspended(self, args, env, job):
        ct, wt = self.ct, self.wt
        class Startup(ct.Structure):
            _fields_ = [('cb', wt.DWORD), ('reserved', wt.LPWSTR),
                        ('desktop', wt.LPWSTR), ('title', wt.LPWSTR)] + [
                (n, wt.DWORD) for n in ('x','y','xs','ys','xc','yc','fill','flags')] + [
                ('show', wt.WORD), ('reserved_size', wt.WORD),
                ('reserved_ptr', ct.c_void_p), ('stdin', wt.HANDLE),
                ('stdout', wt.HANDLE), ('stderr', wt.HANDLE)]
        class StartupEx(ct.Structure):
            _fields_ = [('startup', Startup), ('attributes', ct.c_void_p)]
        class ProcessInfo(ct.Structure):
            _fields_ = [('process', wt.HANDLE), ('thread', wt.HANDLE),
                        ('pid', wt.DWORD), ('tid', wt.DWORD)]
        initialize = self.k.InitializeProcThreadAttributeList
        initialize.argtypes = [ct.c_void_p, wt.DWORD, wt.DWORD, ct.POINTER(ct.c_size_t)]
        initialize.restype = wt.BOOL
        update = self.k.UpdateProcThreadAttribute
        update.argtypes = [ct.c_void_p, wt.DWORD, ct.c_size_t, ct.c_void_p,
                           ct.c_size_t, ct.c_void_p, ct.c_void_p]
        update.restype = wt.BOOL
        delete = self.k.DeleteProcThreadAttributeList
        delete.argtypes = [ct.c_void_p]; delete.restype = None
        create = self.k.CreateProcessW
        create.argtypes = [wt.LPCWSTR, wt.LPWSTR, ct.c_void_p, ct.c_void_p,
                           wt.BOOL, wt.DWORD, ct.c_void_p, wt.LPCWSTR,
                           ct.POINTER(StartupEx), ct.POINTER(ProcessInfo)]
        create.restype = wt.BOOL
        size = ct.c_size_t()
        initialize(None, 2, 0, ct.byref(size))
        attributes = ct.create_string_buffer(size.value)
        self.check(initialize(attributes, 2, 0, ct.byref(size)))
        try:
            jobs = (wt.HANDLE * 1)(job)
            # Windows 10+ JOB_LIST: refusal is detected BEFORE any child starts.
            self.check(update(attributes, 0, 0x0002000D, jobs, ct.sizeof(jobs), None, None))
            keepalive = []
            return self._create_with_attributes(args, env, attributes, StartupEx, ProcessInfo, create, update, keepalive)
        finally:
            delete(attributes)

    def _create_with_attributes(self, args, env, attributes, StartupEx, ProcessInfo, create, update, keepalive):
        import msvcrt
        ct, wt = self.ct, self.wt
        # Explicit handle allowlist: child gets only NUL, never the job handle.
        with open(os.devnull, 'r+b', buffering=0) as null:
            handle = msvcrt.get_osfhandle(null.fileno())
            os.set_handle_inheritable(handle, True)
            handles = (wt.HANDLE * 1)(handle)
            keepalive.append(handles)  # Attribute values outlive DeleteAttributeList.
            self.check(update(attributes, 0, 0x00020002, handles, ct.sizeof(handles), None, None))
            startup = StartupEx()
            startup.startup.cb = ct.sizeof(startup)
            startup.startup.flags = subprocess.STARTF_USESTDHANDLES
            startup.startup.stdin = startup.startup.stdout = startup.startup.stderr = handle
            startup.attributes = ct.cast(attributes, ct.c_void_p)
            info = ProcessInfo()
            command = ct.create_unicode_buffer(subprocess.list2cmdline(args))
            block = ct.create_unicode_buffer('\0'.join(k+'='+v for k,v in sorted(env.items(), key=lambda x: x[0].upper()))+'\0\0')
            self.check(create(None, command, None, None, True,
                              0x00000004 | 0x00080000 | 0x00000400 | subprocess.CREATE_NO_WINDOW,
                              block, None, ct.byref(startup), ct.byref(info)))
        return info.process, info.thread, info.pid


    def resume(self, thread):
        if self.k.ResumeThread(thread) == 0xffffffff:
            raise self.ct.WinError(self.ct.get_last_error())

    def wait_process(self, process, timeout):
        result = self.api.WaitForSingleObject(process, max(0, int(timeout * 1000)))
        if result == self.api.WAIT_TIMEOUT:
            raise subprocess.TimeoutExpired('owned Windows process handle', timeout)
        if result != self.api.WAIT_OBJECT_0:
            raise ProcessCleanupError('process handle wait failed')
        return self.api.GetExitCodeProcess(process)

    def terminate_process(self, process):
        self.api.TerminateProcess(process, 124)

    def terminate_job(self, job):
        try:
            self.retain_members(job)
            self.check(self.k.TerminateJobObject(job, 124))
            # Include children created between the first snapshot and termination.
            self.retain_members(job)
        except BaseException as exc:
            try:
                self.close_observers()
            except ProcessCleanupError as cleanup:
                raise ProcessCleanupError('job termination and observer close failed', owner=self,
                                          errors=[exc, *cleanup.errors]) from exc
            raise

    def close_observers(self):
        self._close_list(self.reap)

    def close_pending(self):
        errors = []
        for handles in (self.reap, self.pending_handles):
            try:
                self._close_list(handles)
            except ProcessCleanupError as exc:
                errors.extend(exc.errors)
        if errors:
            raise ProcessCleanupError('native handle close failed', owner=self, errors=errors) from errors[0]

    def _close_list(self, handles):
        errors = []
        for handle in tuple(handles):
            try:
                self.close(handle)
            except Exception as exc:
                errors.append(exc)
            else:
                handles.remove(handle)
        if errors:
            raise ProcessCleanupError('observer handle close failed', owner=self, errors=errors) from errors[0]

    def retain_members(self, job):
        ct, wt = self.ct, self.wt
        capacity = 64
        while True:
            class Pids(ct.Structure):
                _fields_ = [('assigned', wt.DWORD), ('count', wt.DWORD),
                            ('pids', ct.c_size_t * capacity)]
            data = Pids()
            if self.k.QueryInformationJobObject(job, 3, ct.byref(data), ct.sizeof(data), None):
                break
            if ct.get_last_error() != 234:  # ERROR_MORE_DATA
                raise ct.WinError(ct.get_last_error())
            capacity = max(capacity * 2, data.assigned)
        for pid in data.pids[:data.count]:
            handle = self.k.OpenProcess(0x100000 | 0x1000, False, pid)
            if not handle:
                if ct.get_last_error() == 87:  # exited before OpenProcess
                    continue
                raise ct.WinError(ct.get_last_error())
            try:
                inside = wt.BOOL()
                self.check(self.k.IsProcessInJob(handle, job, ct.byref(inside)))
                # PID reuse cannot authorize any action: only a handle verified
                # in our private job is retained, for read-only waits, not kills.
                if inside.value:
                    self.reap.append(handle)
                    handle = None
            finally:
                if handle is not None:
                    try:
                        self.close(handle)
                    except Exception as exc:
                        self.pending_handles.append(handle)
                        raise ProcessCleanupError('unretained observer close failed', owner=self, errors=[exc]) from exc

    def active(self, job):
        ct, wt = self.ct, self.wt
        class Accounting(ct.Structure):
            _fields_ = [(name, ct.c_longlong) for name in ('user','kernel','period_user','period_kernel')] + [
                (name, wt.DWORD) for name in ('faults','total','active','terminated')]
        data = Accounting()
        self.check(self.k.QueryInformationJobObject(job, 1, ct.byref(data), ct.sizeof(data), None))
        return data.active

    def wait_empty(self, job, timeout):
        deadline = time.monotonic() + timeout
        errors = []
        try:
            while self.active(job):
                if time.monotonic() >= deadline:
                    raise ProcessCleanupError('owned Windows job still has active children')
                time.sleep(0.01)
            # Accounting can reach zero before process teardown signals handles.
            for handle in self.reap:
                self.wait_process(handle, max(0, deadline - time.monotonic()))
        except Exception as exc:
            errors.append(exc)
        try:
            self.close_observers()
        except ProcessCleanupError as exc:
            errors.extend(exc.errors)
        if errors:
            raise ProcessCleanupError('job wait/observer cleanup not confirmed', owner=self, errors=errors) from errors[0]

    def close(self, handle):
        self.api.CloseHandle(handle)
