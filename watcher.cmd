@echo off
REM fomo-radar Watcher (Burst-Erkennung) dauerhaft starten.
REM Wichtig: PYTHONPATH/PYTHONHOME leeren - die Hermes-Umgebung zeigt sonst auf ein
REM fremdes venv, dessen pydantic_core bricht (ImportError: ArgsKwargs).
setlocal
set PYTHONPATH=
set PYTHONHOME=
cd /d O:\Werkstatt\fomo-robinhood-radar
:loop
".venv\Scripts\python.exe" -m fomo_agent.cli watch
timeout /t 10 /nobreak >nul
goto loop
