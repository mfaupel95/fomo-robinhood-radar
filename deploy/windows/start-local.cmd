@echo off
REM Start the local FOMO Radar stack (API + site + bot) if it is not already running.
REM Pure ASCII on purpose - cmd reads .bat files in the ANSI codepage.
setlocal
set ROOT=%~dp0..\..
cd /d "%ROOT%"
set PYTHONIOENCODING=utf-8
set PYTHONPATH=
set PYTHONHOME=
if not exist logs mkdir logs

netstat -ano | findstr /c:":8000 " >nul 2>&1
if errorlevel 1 (
    echo [start] api  -^> logs\api.log
    start "fomo-api" /b /d "%ROOT%" cmd /c ".venv\Scripts\python.exe -m fomo_agent.cli serve >> logs\api.log 2>&1"
) else (
    echo [skip]  api already listening on 8000
)

netstat -ano | findstr /c:":4321 " >nul 2>&1
if errorlevel 1 (
    echo [start] site -^> logs\site.log
    start "fomo-site" /b /d "%ROOT%\site" cmd /c "npm run preview -- --port 4321 --host 127.0.0.1 >> ..\logs\site.log 2>&1"
) else (
    echo [skip]  site already listening on 4321
)

if /i "%~1"=="--no-bot" goto done
REM A second bot exits by itself with 409 (one long-poller per token), so starting it blindly is safe.
echo [start] bot  -^> logs\bot.log
start "fomo-bot" /b /d "%ROOT%" cmd /c ".venv\Scripts\python.exe -m fomo_agent.cli bot >> logs\bot.log 2>&1"

:done
ping -n 3 127.0.0.1 >nul
echo.
echo   site  http://127.0.0.1:4321
echo   api   http://127.0.0.1:8000/docs
echo.
endlocal
