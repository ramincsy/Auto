@echo off
REM Auto Contributions - Local Setup Script for Windows
REM This script sets up your local environment for development

setlocal enabledelayedexpansion

echo.
echo 🚀 Auto Contributions - Local Setup
echo ====================================

REM Check Python version
echo 📦 Checking Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.x
    exit /b 1
)
python --version
echo ✅ Python found

REM Create virtual environment
if not exist "venv\" (
    echo 📝 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📦 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
if exist "requirements.txt" (
    echo 📦 Installing requirements...
    pip install -r requirements.txt
)

REM Install development dependencies
echo 📦 Installing development tools...
pip install black ruff pre-commit

REM Install pre-commit hooks
echo 🔒 Installing pre-commit hooks...
pre-commit install
echo ✅ Pre-commit hooks installed

REM Test the setup
echo.
echo 🧪 Testing setup...
python generate_content.py

echo.
echo ✅ Setup completed successfully!
echo.
echo 📝 Next steps:
echo 1. Activate venv: venv\Scripts\activate.bat
echo 2. Run daily contribution: python generate_content.py
echo 3. Log a note: python scripts/log_daily.py --note "Your note"
echo 4. Create a branch and commit: git checkout -b feature/your-feature
echo.
echo 🔗 GitHub Setup:
echo 1. Create a Fine-Grained PAT at: https://github.com/settings/tokens?type=beta
echo 2. Scopes needed: Contents (Read ^& Write) for this repo only
echo 3. Add to Secrets as: GH_TOKEN2
echo.
echo 💡 For more info, see README.md
