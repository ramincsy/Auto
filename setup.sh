#!/bin/bash

# Auto Contributions - Local Setup Script
# This script sets up your local environment for development

set -e  # Exit on error

echo "🚀 Auto Contributions - Local Setup"
echo "===================================="

# Check Python version
echo "📦 Checking Python..."
python_version=$(python --version 2>&1)
echo "✅ Found: $python_version"

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "📝 Creating virtual environment..."
    python -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip

# Install dependencies
if [ -f "requirements.txt" ]; then
    echo "📦 Installing requirements..."
    pip install -r requirements.txt
fi

# Install development dependencies
echo "📦 Installing development tools..."
pip install black ruff pre-commit

# Install pre-commit hooks
echo "🔒 Installing pre-commit hooks..."
pre-commit install
echo "✅ Pre-commit hooks installed"

# Test the setup
echo ""
echo "🧪 Testing setup..."
python generate_content.py

echo ""
echo "✅ Setup completed successfully!"
echo ""
echo "📝 Next steps:"
echo "1. Activate venv: source venv/bin/activate"
echo "2. Run daily contribution: python generate_content.py"
echo "3. Log a note: python scripts/log_daily.py --note 'Your note'"
echo "4. Create a branch and commit: git checkout -b feature/your-feature"
echo ""
echo "🔗 GitHub Setup:"
echo "1. Create a Fine-Grained PAT at: https://github.com/settings/tokens?type=beta"
echo "2. Scopes needed: Contents (Read & Write) for this repo only"
echo "3. Add to Secrets as: GH_TOKEN2"
echo ""
echo "💡 For more info, see README.md"
