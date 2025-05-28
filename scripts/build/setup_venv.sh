#!/bin/bash
# setup_venv.sh - Script to set up Python virtual environment for ns-3 + MLPL project
# This script creates and configures a Python virtual environment

# Stop on errors
set -e

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

echo "Setting up virtual environment for ns-3 + MLPL research project..."

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed or not in PATH."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Get Python version
PYTHON_VERSION=$(python3 --version)
echo "Found $PYTHON_VERSION"

# Create virtual environment if it doesn't exist
if [ ! -d "$PROJECT_ROOT/venv" ]; then
    echo "Creating virtual environment in $PROJECT_ROOT/venv..."
    python3 -m venv "$PROJECT_ROOT/venv"
    echo "Virtual environment created successfully."
else
    echo "Virtual environment already exists at $PROJECT_ROOT/venv"
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$PROJECT_ROOT/venv/bin/activate"

# Check if activation was successful
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

echo "Installing required packages..."
pip install --upgrade pip
pip install -r "$PROJECT_ROOT/requirements.txt"

echo "Virtual environment setup complete!"
echo ""
echo "To activate this environment later, run:"
echo "  source venv/bin/activate"
echo ""
echo "To deactivate the environment when finished, run:"
echo "  deactivate"

# Keep the virtual environment activated for the current session
