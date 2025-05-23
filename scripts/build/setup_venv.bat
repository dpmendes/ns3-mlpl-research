@echo off
REM setup_venv.bat - Script to set up Python virtual environment for ns-3 + MLPL project
REM This script creates and configures a Python virtual environment on Windows

echo Setting up virtual environment for ns-3 + MLPL research project...

REM Get the script directory and project root
set "SCRIPT_DIR=%~dp0"
set "PROJECT_ROOT=%SCRIPT_DIR%..\..\"

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python is not installed or not in PATH.
    echo Please install Python and try again.
    exit /b 1
)

REM Get Python version
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo Found %PYTHON_VERSION%

REM Create virtual environment if it doesn't exist
if not exist "%PROJECT_ROOT%venv\" (
    echo Creating virtual environment in %PROJECT_ROOT%venv\...
    python -m venv "%PROJECT_ROOT%venv"
    echo Virtual environment created successfully.
) else (
    echo Virtual environment already exists at %PROJECT_ROOT%venv\
)

REM Activate virtual environment
echo Activating virtual environment...
call "%PROJECT_ROOT%venv\Scripts\activate.bat"

REM Check if activation was successful
if "%VIRTUAL_ENV%"=="" (
    echo Error: Failed to activate virtual environment.
    exit /b 1
)

echo Installing required packages...
pip install --upgrade pip
pip install -r "%PROJECT_ROOT%requirements.txt"

echo Virtual environment setup complete!
echo.
echo To activate this environment later, run:
echo   venv\Scripts\activate
echo.
echo To deactivate the environment when finished, run:
echo   deactivate

REM Keep the virtual environment activated for the current session
