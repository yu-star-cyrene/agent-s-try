@echo off
setlocal EnableExtensions EnableDelayedExpansion

cd /d "%~dp0"

git rev-parse --is-inside-work-tree >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Current directory is not a Git repository.
    if not defined NO_PAUSE pause
    exit /b 1
)

if /I not "%SKIP_PRIVATE_ENCRYPT%"=="1" (
    echo.
    echo [ENCRYPT] Building encrypted private bundle before publishing
    echo [ENCRYPT] You will be asked for the shared project key.
    call "%~dp0tools\encrypt_private.bat" --remove-plaintext
    if errorlevel 1 goto :error
) else (
    echo.
    echo [ENCRYPT] SKIP_PRIVATE_ENCRYPT=1, private encryption step skipped.
)

git status --porcelain >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Failed to read Git status. Please check that Git is installed.
    if not defined NO_PAUSE pause
    exit /b 1
)

set "HAS_CHANGES="
for /f "delims=" %%i in ('git status --porcelain') do (
    set "HAS_CHANGES=1"
)

if not defined HAS_CHANGES (
    echo No changes to commit.
    git status --short --branch
    if not defined NO_PAUSE pause
    exit /b 0
)

set "COMMIT_MSG=%~1"
if not defined COMMIT_MSG (
    set /p "COMMIT_MSG=Enter commit message (press Enter to use a timestamp): "
)

if not defined COMMIT_MSG (
    for /f %%i in ('powershell -NoProfile -Command "Get-Date -Format ''yyyy-MM-dd HH:mm:ss''"') do (
        set "NOW=%%i"
    )
    set "COMMIT_MSG=update: !NOW!"
)

for /f "delims=" %%i in ('git branch --show-current') do (
    set "BRANCH=%%i"
)

if not defined BRANCH (
    set "BRANCH=main"
)

echo.
echo [1/4] Current status
git status --short --branch
if errorlevel 1 goto :error

echo.
echo [2/4] Staging changes
git add .
if errorlevel 1 goto :error

echo.
echo [3/4] Creating commit
git commit -m "!COMMIT_MSG!"
if errorlevel 1 goto :error

echo.
echo [4/4] Pushing to GitHub
git push -u origin !BRANCH!
if errorlevel 1 goto :error

echo.
echo Upload complete. Branch: !BRANCH!
if not defined NO_PAUSE pause
exit /b 0

:error
echo.
echo Upload failed. Please review the error output above.
if not defined NO_PAUSE pause
exit /b 1
