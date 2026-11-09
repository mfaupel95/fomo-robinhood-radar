"""Deterministic cleanup faults and native owned-tree lifecycle evidence."""
import subprocess
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import sys
import time

import pytest
from fomo_agent import collector as co, db, credit_guard as cg
from fomo_agent.config import settings


def test_taskkill_timeout_is_transient():
    assert co.classify(subprocess.TimeoutExpired(['taskkill', '/T'], 15)) == 'transient'


@pytest.mark.parametrize('failure', ['taskkill_timeout', 'child_survives'])
def test_cleanup_failure_does_not_permanently_block_or_refund(tmp_path, monkeypatch, failure):
    p = tmp_path/'cleanup.db'
    monkeypatch.setattr(settings, 'db_path', p)
    c = db.connect(p)
    cg.reserve(1000, p)
    monkeypatch.setattr(co, 'build_steps', lambda: {'holdings': (3600, None)})
    def runner(args, timeout):
        with co.SingleInstance(str(p)+'.worker'):
            if failure == 'taskkill_timeout':
                raise subprocess.TimeoutExpired(['taskkill', '/T'], 15)
            raise co.ProcessCleanupError('owned child still active')
    try:
        with co.SingleInstance(p):
            assert co.run_due(c, ['holdings'], runner=runner) == 1
        row = c.execute('SELECT reason,next_at FROM sammler_recovery').fetchone()
        assert row['reason'] == 'transient'
        assert 0 < row['next_at'] - db.now() <= 60
        assert c.execute('SELECT used FROM fomo_credit_month').fetchone()[0] == 1000
        assert c.execute('SELECT error FROM runs').fetchone()[0] == 'transient'
        with co.SingleInstance(p), co.SingleInstance(str(p)+'.worker'):
            pass
        with pytest.raises(cg.BudgetBlocked):
            cg.reserve(1, p)
    finally:
        c.close()


def test_atomic_owned_startup_resume_failure_reaps():
    from fomo_agent.process_lifecycle import WindowsTree, ProcessCleanupError
    events = []
    class Native:
        def create_job(self): events.append('job'); return 10
        def spawn_suspended(self, args, env, job):
            assert job == 10
            events.append('atomic_owned'); return 20, 30, 40
        def resume(self, thread): events.append('resume_refused'); raise OSError('fixture resume refused')
        def terminate_process(self, process): events.append('terminate_owned_handle')
        def wait_process(self, process, timeout): events.append('reaped'); return 124
        def close(self, handle): events.append(('close', handle))
    with pytest.raises(ProcessCleanupError):
        WindowsTree(['fixture'], {}, native=Native())
    assert 'resume' not in events
    assert events.index('atomic_owned') < events.index('resume_refused') < events.index('terminate_owned_handle') < events.index('reaped')
    assert {e[1] for e in events if isinstance(e, tuple)} == {10, 20, 30}


def test_tree_survivor_is_reported_not_success():
    from fomo_agent.process_lifecycle import WindowsTree, ProcessCleanupError
    events = []
    class Native:
        def create_job(self): return 10
        def spawn_suspended(self, args, env, job):
            assert job == 10
            events.append('atomic_owned'); return 20, 30, 40
        def resume(self, thread): events.append('resume')
        def terminate_job(self, job): events.append('terminate_job')
        def wait_empty(self, job, timeout): raise ProcessCleanupError('fixture child survives')
        def close(self, handle): events.append(('close', handle))
    tree = WindowsTree(['fixture'], {}, native=Native())
    with pytest.raises(ProcessCleanupError):
        tree.close()
    assert events[:2] == ['atomic_owned', 'resume']
    assert ('close', 10) in events and ('close', 20) in events


@pytest.mark.parametrize('root_exit', ['no', 'yes', 'cleanup_fault'])
def test_native_launcher_child_grandchild_handles_and_lock(tmp_path, root_exit):
    from fomo_agent.process_lifecycle import WindowsTree
    k = ctypes.WinDLL('kernel32', use_last_error=True)
    k.OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
    k.OpenProcess.restype = wintypes.HANDLE
    k.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
    k.IsProcessInJob.argtypes = [wintypes.HANDLE, wintypes.HANDLE, ctypes.POINTER(wintypes.BOOL)]
    script = Path(__file__).parent/'fixtures/owned_tree.py'
    lock = tmp_path/'grandchild.lock'
    env = dict(os.environ)
    env.pop('PYTHONHOME', None)
    before = time.monotonic()
    tree = WindowsTree([sys.executable, str(script), 'root', str(tmp_path), str(lock), root_exit], env)
    handles, records = [], []
    def created(handle):
        values = [wintypes.FILETIME() for _ in range(4)]
        assert k.GetProcessTimes(handle, *(ctypes.byref(x) for x in values))
        return values[0].dwLowDateTime | (values[0].dwHighDateTime << 32)
    try:
        deadline = time.monotonic()+5
        while not (tmp_path/'locked').exists():
            assert time.monotonic()<deadline, 'fixture did not become ready'
            time.sleep(.01)
        for role in ('root','child','grandchild'):
            record = json.loads((tmp_path/(role+'.json')).read_text())
            handle = k.OpenProcess(0x100000 | 0x1000, False, record['pid'])
            # Root can exit normally; its launcher handle is retained by tree.
            if not handle and root_exit == 'yes' and role == 'root':
                continue
            assert handle
            handles.append(handle)
            assert created(handle) == record['created']
            inside = wintypes.BOOL()
            assert k.IsProcessInJob(handle, tree.job, ctypes.byref(inside)) and inside.value
            records.append(dict(record, handle_creation_time=created(handle), in_job=True))
        # Retain handles for every member, including the Windows venv launchers.
        class Pids(ctypes.Structure):
            _fields_ = [('assigned',wintypes.DWORD),('count',wintypes.DWORD),('pids',ctypes.c_size_t*32)]
        data = Pids()
        tree.native.check(k.QueryInformationJobObject(tree.job,3,ctypes.byref(data),ctypes.sizeof(data),None))
        assert data.count >= 4, 'real launcher and descendants required'
        for pid in data.pids[:data.count]:
            handle = k.OpenProcess(0x100000 | 0x1000, False, pid)
            if not handle:
                continue  # an already exited member cannot be a survivor
            handles.append(handle)
            records.append(dict(role='job_member',pid=pid,handle_creation_time=created(handle)))
        if root_exit == 'yes':
            assert tree.wait(2) == 0
        else:
            with pytest.raises(subprocess.TimeoutExpired):
                tree.wait(.3)
        empty = []
        original_wait_empty = tree.native.wait_empty
        def observed_wait_empty(job, timeout):
            original_wait_empty(job, timeout)
            empty.append(tree.native.active(job))
        tree.native.wait_empty = observed_wait_empty
        if root_exit == 'cleanup_fault':
            def fail_terminate(job):
                raise OSError('deterministic TerminateJobObject fault')
            tree.native.terminate_job = fail_terminate
            with pytest.raises(co.ProcessCleanupError):
                tree.close()
            # Independent last-handle-close fallback; never report success from it.
            for handle in handles:
                assert tree.native.api.WaitForSingleObject(handle,3000) == 0
        else:
            tree.close()
            assert empty == [0]
        for handle in handles:
            assert tree.native.api.WaitForSingleObject(handle,0) == 0
        for record in records:
            record['signaled_after_cleanup'] = True
        with co.SingleInstance(str(lock)+'.probe'):
            pass
        import msvcrt
        with open(lock,'r+b') as f:
            msvcrt.locking(f.fileno(),msvcrt.LK_NBLCK,1)
            msvcrt.locking(f.fileno(),msvcrt.LK_UNLCK,1)
        assert time.monotonic()-before < 10
        evidence = dict(root_exit=root_exit,seconds=time.monotonic()-before,job_active_after=empty[0] if empty else 'unconfirmed; handles signaled',lock_reacquired=True,processes=records)
        (tmp_path/'native-evidence.json').write_text(json.dumps(evidence,indent=2))
        print('NATIVE_TREE_EVIDENCE '+json.dumps(evidence))
    finally:
        tree.close()
        for handle in handles:
            tree.native.close(handle)
