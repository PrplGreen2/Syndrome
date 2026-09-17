@echo off
REM Get the directory where this BAT file is located
set SCRIPT_DIR=%~dp0

REM Run the Python script from the same directory
python "%SCRIPT_DIR%1x1_replacer.py"

pause
