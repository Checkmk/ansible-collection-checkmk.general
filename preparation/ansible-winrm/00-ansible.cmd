@echo off
set CURRENT_PATH=%~dp0
echo %CURRENT_PATH%

rem https://stackoverflow.com/questions/4051883/batch-script-how-to-check-for-admin-rights
goto check_Permissions

:check_Permissions
    echo Administrative permissions required. Detecting permissions...
    
    net session >nul 2>&1
    if %errorLevel% == 0 (
        echo Success: Administrative permissions confirmed. Setting up everything for Ansible...
        %CURRENT_PATH%\01-winrm-quickconfig.cmd & %CURRENT_PATH%\02-ansible-winrm.cmd & %CURRENT_PATH%\03-allow-icmp.cmd
pause
    ) else (
        echo Failure: Current permissions inadequate. You need to run this script as administrator!
    )

pause >nul
