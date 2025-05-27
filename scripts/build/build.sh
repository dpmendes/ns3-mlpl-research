# scripts/build/build.sh

#!/bin/bash
# Main build script for ns3-mlpl-research project

# Exit on error
set -e

echo "Building ns3-mlpl-research project..."

# Ensure we're in the project root directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
PROJECT_ROOT="$( cd "$SCRIPT_DIR/../.." &> /dev/null && pwd )"
cd "$PROJECT_ROOT"

# Check if virtual environment is active
if [[ -z "$VIRTUAL_ENV" ]]; then
    echo "Warning: No virtual environment detected. It's recommended to run this script within"
    echo "the project's virtual environment. You can activate it with:"
    echo "  source venv/bin/activate  # On Linux/macOS"
    echo "  venv\\Scripts\\activate     # On Windows"
    
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create directories if they don't exist
echo "Creating required directories..."
mkdir -p build

# Check for ns-3 installation
if ! python -c "import ns.core" &> /dev/null; then
    echo "Error: ns-3 Python bindings not found."
    echo "Please install ns-3 with Python bindings and make sure it's in your PYTHONPATH."
    echo "See installation instructions in docs/ENVIRONMENT.md"
    exit 1
fi

# Build any C++ extensions if needed
echo "Building C++ extensions..."
python setup.py build_ext --inplace

# Install in development mode
echo "Installing in development mode..."
pip install -e .

echo "Build completed successfully!"
echo
echo "You can now run the examples:"
echo "  python src/examples/basic_mlpl_example.py"
