@echo off
setlocal

cd /d "%~dp0\.."

powershell -NoProfile -ExecutionPolicy Bypass -File "tools\decrypt_private.ps1" -Overwrite
exit /b %ERRORLEVEL%
