@echo off
echo Running Weather Dashboard Tests...
echo.

cd /d "%~dp0"

REM Check if virtual environment exists
if exist venv\Scripts\activate.bat (
    call venv\Scripts\activate.bat
) else (
    echo Warning: No virtual environment found. Using system Python.
)

REM Install test dependencies if needed
pip install pytest requests-mock

REM Run tests
python -m pytest tests/ -v --tb=short

REM Deactivate virtual environment if it was activated
if exist venv\Scripts\activate.bat (
    call deactivate
)

echo.
echo Tests completed.
pause