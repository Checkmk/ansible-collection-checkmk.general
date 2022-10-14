@echo off
set CURRENT_PATH=%~dp0
echo %CURRENT_PATH%
powershell Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
powershell %CURRENT_PATH%\ConfigureRemotingForAnsible.ps1