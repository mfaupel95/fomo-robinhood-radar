@echo off
REM Register the local stack at logon (Task Scheduler, current user, no admin needed).
REM Undo:  schtasks /Delete /TN "FOMO Radar local" /F
setlocal
set HERE=%~dp0
schtasks /Create /TN "FOMO Radar local" /TR "wscript.exe \"%HERE%fomo-local-hidden.vbs\"" /SC ONLOGON /RL LIMITED /F
if errorlevel 1 (
    echo could not create the task - run this file as administrator once
    exit /b 1
)
echo.
schtasks /Query /TN "FOMO Radar local" /FO LIST | findstr /i "TaskName Status Next"
endlocal
