"""Windows owned process trees: suspend -> assign private job -> resume.

No PID enumeration/kill and no taskkill helper. Descendants inherit membership;
no breakaway flag is permitted. The non-inheritable job handle is kill-on-close,
including when the supervisor crashes. Failure to assign is fail-closed while
only the retained, never-resumed process handle can be terminated.
"""
from __future__ import annotations
import os
import subprocess
import time


class ProcessCleanupError(RuntimeError):
    """The owned process tree could not be safely started or reaped (transient)."""


class WindowsTree:
    def __init__(self, args, env, native=None):
        self.native = native if native is not None else _Native()
        self.job = self.process = self.thread = None
        self.pid = None
        try:
            self.job = self.native.create_job()
            self.process, self.thread, self.pid = self.native.spawn_suspended(args, env)
            self.native.assign(self.job, self.process)
            self.native.resume(self.thread)
            self.native.close(self.thread)
            self.thread = None
        except BaseException as exc:
            try:
                if self.process is not None:
                    self.native.terminate_process(self.process)
                    self.native.wait_process(self.process, 3)
            except Exception as cleanup_exc:
                raise ProcessCleanupError('Windows suspended process cleanup not confirmed') from cleanup_exc
            finally:
                for name in ('thread', 'process', 'job'):
                    handle = getattr(self, name)
                    if handle is not None:
                        self.native.close(handle)
                        setattr(self, name, None)
            raise ProcessCleanupError('Windows tree startup failed closed') from exc

    def wait(self, timeout):
        return self.native.wait_process(self.process, timeout)

    def close(self):
        if self.job is None:
            return
        try:
            # Also reap descendants after a normal launcher exit.
            self.native.terminate_job(self.job)
            self.native.wait_empty(self.job, 3)
        except Exception as exc:
            raise ProcessCleanupError('Windows job cleanup not confirmed') from exc
        finally:
            # Closing the last job handle is an independent kernel kill fallback.
            # Do not turn an unconfirmed cleanup into a successful return.
            for name in ('thread', 'process', 'job'):
                handle = getattr(self, name)
                if handle is not None:
                    self.native.close(handle)
                    setattr(self, name, None)


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
        self.k = ct.WinDLL('kernel32', use_last_error=True)
        signatures = {
            'CreateJobObjectW': ([ct.c_void_p, wt.LPCWSTR], wt.HANDLE),
            'SetInformationJobObject': ([wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD], wt.BOOL),
            'QueryInformationJobObject': ([wt.HANDLE, ct.c_int, ct.c_void_p, wt.DWORD, ct.c_void_p], wt.BOOL),
            'AssignProcessToJobObject': ([wt.HANDLE, wt.HANDLE], wt.BOOL),
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
            self.close(job)
            raise

    def spawn_suspended(self, args, env):
        import msvcrt
        # Explicit handle allowlist: child gets only NUL, never the job handle.
        with open(os.devnull, 'r+b', buffering=0) as null:
            handle = msvcrt.get_osfhandle(null.fileno())
            os.set_handle_inheritable(handle, True)
            startup = subprocess.STARTUPINFO()
            startup.dwFlags = subprocess.STARTF_USESTDHANDLES
            startup.hStdInput = startup.hStdOutput = startup.hStdError = handle
            startup.lpAttributeList = {'handle_list': [handle]}
            hp, ht, pid, tid = self.api.CreateProcess(
                None, subprocess.list2cmdline(args), None, None, True,
                0x00000004 | subprocess.CREATE_NO_WINDOW, env, None, startup)
        return hp, ht, pid

    def assign(self, job, process):
        self.check(self.k.AssignProcessToJobObject(job, process))

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
        except BaseException:
            for handle in self.reap:
                self.close(handle)
            self.reap.clear()
            raise

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
                    self.close(handle)

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
        try:
            while self.active(job):
                if time.monotonic() >= deadline:
                    raise ProcessCleanupError('owned Windows job still has active children')
                time.sleep(0.01)
            # Accounting can reach zero before process teardown signals handles.
            for handle in self.reap:
                self.wait_process(handle, max(0, deadline - time.monotonic()))
        finally:
            for handle in self.reap:
                self.close(handle)
            self.reap.clear()

    def close(self, handle):
        self.api.CloseHandle(handle)
