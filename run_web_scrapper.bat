@echo off

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt

rem Check the exit code of the dependency installation
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies. Test cases and project will not be executed.
    pause
    exit /b
)

set PYTHONPATH=%~dp0

echo Running test cases...
python -m unittest discover

rem Check the exit code of the test execution
if %ERRORLEVEL% EQU 0 (
    echo All test cases passed. Running the project...
    python src\main.py
) else (
    echo Test cases failed. The project will not be executed.
)

pause
