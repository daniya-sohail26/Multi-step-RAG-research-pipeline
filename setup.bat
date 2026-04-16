@echo off
REM Agentic AI Research Assistant - Automated Setup Script for Windows
REM This script automates the entire setup process

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  Agentic AI Research Assistant - Setup Wizard                 ║
echo ║  Windows Edition                                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM Check Python installation
echo [1/5] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Download from: https://www.python.org/downloads/
    echo    Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% found
echo.

REM Check if .env exists
echo [2/5] Checking environment configuration...
if exist .env (
    echo ✓ .env file found
) else (
    echo ⚠  .env file not found, creating from template...
    if exist .env.example (
        copy .env.example .env
        echo ✓ .env created from .env.example
        echo.
        echo ⚠️  IMPORTANT: You need to add your API keys to .env
        echo    1. Go to https://makersuite.google.com/app/apikey
        echo    2. Create an API key and copy it
        echo    3. Go to https://serpapi.com/signup
        echo    4. Sign up and copy your API key
        echo    5. Edit .env and paste the keys
        echo.
        start notepad .env
        echo    .env is open in Notepad - please add your API keys
        pause
    ) else (
        echo ❌ .env.example not found!
        pause
        exit /b 1
    )
)
echo.

REM Create virtual environment
echo [3/5] Setting up Python virtual environment...
if exist venv (
    echo ✓ Virtual environment already exists
) else (
    echo Creating new virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
)
echo.

REM Activate virtual environment
echo [4/5] Activating virtual environment and installing dependencies...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ❌ Failed to activate virtual environment
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo Installing required packages (this may take 2-3 minutes)...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    echo    Try running: pip install -r requirements.txt
    pause
    exit /b 1
)
echo ✓ All dependencies installed
echo.

REM Verify installation
echo [5/5] Verifying installation...
python -c "import streamlit; import langchain; import faiss" 2>nul
if errorlevel 1 (
    echo ⚠️  Warning: Some packages may not have installed correctly
    echo    Try running: pip install -r requirements.txt
) else (
    echo ✓ All packages verified
)
echo.

REM Summary and next steps
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  Setup Complete! ✓                                            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo Next Steps:
echo.
echo 1. Verify your API keys are in .env file
echo    - GOOGLE_API_KEY (from https://makersuite.google.com/app/apikey)
echo    - SERPAPI_API_KEY (from https://serpapi.com)
echo.
echo 2. Start the application:
echo    ► Option A - Run this script again with 'run' parameter:
echo      setup.bat run
echo    ► Option B - Run manually:
echo      venv\Scripts\activate
echo      streamlit run app.py
echo.
echo 3. Open http://localhost:8501 in your browser
echo.
echo 4. Start researching! Try queries like:
echo    - "Latest AI trends"
echo    - "Quantum computing basics"
echo    - "Machine learning in healthcare"
echo.

REM Check if user wants to run the app immediately
if "%1"=="run" (
    echo Starting application...
    streamlit run app.py
) else (
    echo.
    echo To start the application now, run:
    echo   setup.bat run
    echo.
    pause
)
