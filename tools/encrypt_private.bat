@echo off
setlocal

cd /d "%~dp0\.."

set "REMOVE_FLAG="
if /I "%~1"=="--remove-plaintext" set "REMOVE_FLAG=-RemovePlaintext"

powershell -NoProfile -ExecutionPolicy Bypass -File "tools\encrypt_private.ps1" %REMOVE_FLAG%
exit /b %ERRORLEVEL%
