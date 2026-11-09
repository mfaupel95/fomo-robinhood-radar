"""Review-v2 acceptance: atomic creation and independently attempted closes."""
import inspect
import ctypes as ct
from ctypes import wintypes as wt
import json, os, subprocess, sys, time
from pathlib import Path
import pytest
from fomo_agent.process_lifecycle import WindowsTree, ProcessCleanupError, _Native
from fomo_agent.collector import classify


def test_creation_has_no_separate_assign_window():
    source = inspect.getsource(WindowsTree.__init__)
    assert 'self.native.assign(' not in source
    assert 'self.job)' in source
    assert '0x0002000D' in inspect.getsource(_Native.spawn_suspended)


@pytest.mark.parametrize('phase', ['create', 'spawn', 'resume', 'terminate_process',
    'startup_wait', 'terminate_job', 'wait_empty', 'close_thread_once',
    'close_process_once', 'close_job_once'])
def test_review_fault_matrix(phase):
    events = []
    class Native:
        closed_fault = False
        def fault(self, stage):
            events.append(stage)
            if phase == stage: raise OSError('injected '+stage)
        def create_job(self): self.fault('create'); return 10
        def spawn_suspended(self, args, env, job):
            assert job == 10
            self.fault('spawn'); return 20,30,40
        def resume(self, t):
            self.fault('resume')
            if phase in ('terminate_process', 'startup_wait'): raise OSError('rollback')
        def terminate_process(self, p): self.fault('terminate_process')
        def wait_process(self, p, t): self.fault('startup_wait'); return 124
        def terminate_job(self, j): self.fault('terminate_job')
        def wait_empty(self, j, t): self.fault('wait_empty')
        def close(self, h):
            events.append('close:'+str(h))
            if phase == {30:'close_thread_once',20:'close_process_once',10:'close_job_once'}[h] and not self.closed_fault:
                self.closed_fault = True
                raise OSError('CloseHandle')
    native = Native()
    with pytest.raises(ProcessCleanupError) as raised:
        tree = WindowsTree(['fixture'], {}, native=native)
        tree.close()
    assert classify(raised.value) == 'transient'
    if phase not in ('create',): assert 'close:10' in events
    if phase == 'close_process_once': assert events.index('close:20') < events.index('close:10')
    print('CLOSE_FAULT_V3 '+json.dumps(dict(phase=phase, events=events, classification=classify(raised.value))))
    owner = raised.value.owner
    native.close = lambda h: None
    native.terminate_job = lambda j: None
    native.wait_empty = lambda j,t: None
    owner.close()


@pytest.mark.parametrize('failed', [10, 20])
def test_close_fault_is_transient_attempts_all_and_retains_ownership(failed):
    events = []
    class Native:
        def create_job(self): return 10
        def spawn_suspended(self, *args): return 20, 30, 40
        def assign(self, *args): pass
        def resume(self, *args): pass
        def terminate_job(self, *args): pass
        def wait_empty(self, *args): pass
        def close(self, h):
            events.append(h)
            if h == failed: raise OSError('review-v2 close fault')
    tree = WindowsTree(['fixture'], {}, native=Native())
    with pytest.raises(ProcessCleanupError) as raised:
        tree.close()
    assert classify(raised.value) == 'transient'
    assert 20 in events and 10 in events
    assert getattr(tree, 'job' if failed == 10 else 'process') == failed
    assert raised.value.owner is tree
    from fomo_agent.process_lifecycle import _pending_owners
    assert tree in _pending_owners
    tree.native.close = lambda h: events.append(h)
    tree.close()
    assert tree.job is None and tree.process is None
    assert tree not in _pending_owners


def test_job_attribute_unsupported_fails_before_create(tmp_path):
    native = _Native()
    attempted = []
    def unsupported(*args):
        attempted.append(args[2])
        ct.set_last_error(50)
        return 0
    native.k.UpdateProcThreadAttribute = unsupported
    native._create_with_attributes = lambda *args: pytest.fail('CreateProcess attempted on unsupported OS')
    with pytest.raises(ProcessCleanupError) as raised:
        WindowsTree([sys.executable, '-c', 'raise AssertionError()'], {}, native=native)
    assert attempted == [0x0002000D]
    assert classify(raised.value) == 'transient'
    assert raised.value.owner.job is None


def test_startup_multiple_close_faults_keep_every_handle():
    events = []
    class Native:
        def create_job(self): return 10
        def spawn_suspended(self, *args): return 20, 30, 40
        def resume(self, t): raise OSError('resume')
        def terminate_process(self, p): events.append('terminate')
        def wait_process(self, p, t): events.append('wait')
        def close(self, h): events.append(h); raise OSError(str(h))
    with pytest.raises(ProcessCleanupError) as raised:
        WindowsTree(['fixture'], {}, native=Native())
    tree = raised.value.owner
    assert events == ['terminate', 'wait', 30, 20, 10]
    assert len(raised.value.errors) == 4
    assert (tree.thread, tree.process, tree.job) == (30, 20, 10)
    assert classify(raised.value) == 'transient'
    tree.native.close = lambda h: None
    tree.native.terminate_job = lambda j: None
    tree.native.wait_empty = lambda j,t: None
    tree.close()


def test_observer_close_fault_retains_only_failed_handle_and_tries_rest():
    native = _Native()
    native.reap = [101, 102, 103]
    seen = []
    def fail(h):
        seen.append(h)
        if h == 102: raise OSError('observer close')
    native.close = fail
    with pytest.raises(ProcessCleanupError) as raised:
        native.close_observers()
    assert seen == [101,102,103]
    assert native.reap == [102]
    assert raised.value.owner is native
    native.close = lambda h: None
    native.close_pending()
    assert not native.reap


@pytest.mark.parametrize('mode', ['before_create', 'after_create'])
def test_native_supervisor_crash_at_creation(tmp_path, mode):
    native = _Native()
    native.k.GetProcessTimes.argtypes = [wt.HANDLE] + [ct.POINTER(wt.FILETIME)]*4
    fixture = Path(__file__).parent/'fixtures/crash_v3.py'
    supervisor = subprocess.Popen([sys.executable, '-B', str(fixture), str(tmp_path), mode], env=dict(os.environ))
    handle = None
    try:
        deadline = time.monotonic()+12
        while not (tmp_path/'ready.json').exists():
            assert supervisor.poll() is None
            assert time.monotonic() < deadline
            time.sleep(.01)
        record = json.loads((tmp_path/'ready.json').read_text())
        if record['pid']:
            handle = native.k.OpenProcess(0x100000|0x1000|1, False, record['pid'])
            assert handle
            values = [wt.FILETIME() for _ in range(4)]
            assert native.k.GetProcessTimes(handle, *(ct.byref(v) for v in values))
            assert record['created'] == values[0].dwLowDateTime | values[0].dwHighDateTime << 32
        supervisor.terminate(); supervisor.wait(5)
        if handle:
            record['wait_after_crash'] = native.api.WaitForSingleObject(handle, 2000)
        record['marker'] = (tmp_path/'executed').exists()
        (tmp_path/'crash-evidence.json').write_text(json.dumps(record, indent=2))
        print('CRASH_V3 '+json.dumps(record))
        assert not record['marker']
        assert not record['job_inheritable']
        if handle:
            assert record['wait_after_crash'] == 0
            assert record['job_active'] == 1
        else:
            assert record['job_active'] == 0
    finally:
        if supervisor.poll() is None: supervisor.terminate(); supervisor.wait(5)
        if handle:
            if native.api.WaitForSingleObject(handle, 0) == 258:
                native.terminate_process(handle); native.wait_process(handle, 3)
            native.close(handle)
