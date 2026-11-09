"""Only the test supervisor and its owned fixture process are stopped."""
import ctypes as ct
from ctypes import wintypes as wt
import json, os, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from fomo_agent.process_lifecycle import _Native, WindowsTree
root = Path(sys.argv[1]); mode = sys.argv[2]
k = ct.WinDLL('kernel32', use_last_error=True)
k.GetProcessTimes.argtypes = [wt.HANDLE] + [ct.POINTER(wt.FILETIME)]*4
k.GetHandleInformation.argtypes = [wt.HANDLE, ct.POINTER(wt.DWORD)]
class Gate(_Native):
    def gate(self, p=None, pid=None):
        record = dict(pid=pid, job_active=self.active(self.job))
        flags = wt.DWORD()
        assert k.GetHandleInformation(self.job, ct.byref(flags))
        record['job_inheritable'] = bool(flags.value & 1)
        if p:
            times = [wt.FILETIME() for _ in range(4)]
            assert k.GetProcessTimes(p, *(ct.byref(x) for x in times))
            record['created'] = times[0].dwLowDateTime | times[0].dwHighDateTime << 32
        (root/'ready.json').write_text(json.dumps(record))
        time.sleep(45)
    def create_job(self):
        self.job = super().create_job(); return self.job
    def _create_with_attributes(self, args, env, attributes, StartupEx, ProcessInfo, create, update, keepalive):
        def gated_create(*call_args):
            if mode == 'before_create': self.gate()
            result = create(*call_args)
            self.check(result)
            info = call_args[-1]._obj
            self.gate(info.process, info.pid)
            return result
        return super()._create_with_attributes(args, env, attributes, StartupEx, ProcessInfo, gated_create, update, keepalive)
WindowsTree([sys.executable, '-I', '-c', 'from pathlib import Path; Path('+repr(str(root/'executed'))+').touch()'], dict(os.environ), native=Gate())
