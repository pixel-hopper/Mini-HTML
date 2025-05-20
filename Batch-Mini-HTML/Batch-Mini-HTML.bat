@echo off
cd /d "%~dp0"

REM Use full path to python executable
where python >nul 2>nul
if errorlevel 1 (
    echo Python is not installed or not in PATH.
    pause
    exit /b
)

python "%~dp0Batch-Mini-HTML.py"
pause
