#!/bin/bash
# hotswap_python.sh - Script to install and switch to Python 3.10 in GitHub Codespaces

set -e

echo "Hotswapping Python version to 3.10..."

# Install pyenv if it's not already installed
if ! command -v pyenv &> /dev/null; then
    echo "Installing pyenv..."
    curl https://pyenv.run | bash
    
    # Add pyenv to PATH for this session
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
    
    # Add pyenv to shell profile for future sessions
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
    echo 'eval "$(pyenv init -)"' >> ~/.bashrc
    echo 'eval "$(pyenv virtualenv-init -)"' >> ~/.bashrc
else
    echo "pyenv is already installed"
    export PYENV_ROOT="$HOME/.pyenv"
    export PATH="$PYENV_ROOT/bin:$PATH"
    eval "$(pyenv init -)"
    eval "$(pyenv virtualenv-init -)"
fi

# Install Python 3.10.13 (latest stable 3.10.x)
echo "Installing Python 3.10.13..."
pyenv install 3.10.13

# Set Python 3.10.13 as global default
echo "Setting Python 3.10.13 as global default..."
pyenv global 3.10.13

# Verify the installation
echo "Verifying Python installation..."
python3 --version
python --version

# Update pip
echo "Updating pip..."
python -m pip install --upgrade pip

echo "Python hotswap complete!"
echo "Current Python version: $(python --version)"
echo ""
echo "Note: You may need to restart your terminal or run 'source ~/.bashrc' to ensure"
echo "the new Python version is available in all terminal sessions."