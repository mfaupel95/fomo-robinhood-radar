"""Only invoked by owned-tree tests; no application imports or I/O beyond fixture."""
import ctypes
from ctypes import wintypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time

role, evidence, lock, root_exit = sys.argv[1:]
k = ctypes.WinDLL('kernel32', use_last_error=True)
k.GetCurrentProcess.restype = wintypes.HANDLE
k.GetProcessTimes.argtypes = [wintypes.HANDLE] + [ctypes.POINTER(wintypes.FILETIME)] * 4
values = [wintypes.FILETIME() for _ in range(4)]
assert k.GetProcessTimes(k.GetCurrentProcess(), *(ctypes.byref(x) for x in values))
created = (values[0].dwHighDateTime << 32) | values[0].dwLowDateTime
# One file per role avoids append interleaving between unrelated handles.
Path(evidence, role+'.json').write_text(json.dumps(dict(role=role,pid=os.getpid(),created=created)))
if role in ('root', 'child'):
    child_role = 'child' if role == 'root' else 'grandchild'
    subprocess.Popen([sys.executable, __file__, child_role, evidence, lock, root_exit])
if role == 'grandchild':
    import msvcrt
    f = open(lock, 'a+b')
    f.write(b'0'); f.flush(); f.seek(0)
    msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
    Path(evidence, 'locked').write_text('ready')
if role == 'root' and root_exit == 'yes':
    deadline = time.monotonic()+5
    while not Path(evidence, 'locked').exists():
        assert time.monotonic()<deadline
        time.sleep(.01)
    sys.exit(0)
time.sleep(60)
