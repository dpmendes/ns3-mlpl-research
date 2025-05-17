# Environment Setup and Management

This document provides detailed instructions for setting up and managing development environments for the ns3-mlpl-research project.

## Option 1: Python Virtual Environment (Recommended for Local Development)

### Setup

#### On Linux/macOS:

```bash
# Make the setup script executable
chmod +x setup_venv.sh

# Run the setup script
./setup_venv.sh
```

#### On Windows:

```cmd
# Run the setup script
setup_venv.bat
```

### Usage

#### On Linux/macOS:

```bash
# Activate the virtual environment
source venv/bin/activate

# Run your code
python src/examples/example_script.py

# When finished, deactivate the virtual environment
deactivate
```

#### On Windows:

```cmd
# Activate the virtual environment
venv\Scripts\activate

# Run your code
python src\examples\example_script.py

# When finished, deactivate the virtual environment
deactivate
```

### Updating Dependencies

If you need to add new dependencies:

1. Add them to `requirements.txt`
2. Run:
   ```bash
   pip install -r requirements.txt
   ```

## Option 2: Docker (For Containerized Development)

Once Docker support is available on your system, you can use the provided Dockerfile:

```bash
# Build the Docker image
docker build -t ns3-mlpl-research .

# Run a container
docker run -it --name ns3-mlpl --volume $(pwd):/app ns3-mlpl-research bash
```

## Option 3: GitHub Codespaces (For Cloud Development)

1. Go to your GitHub repository
2. Click the "Code" button
3. Select the "Codespaces" tab
4. Click "Create codespace on main"

## Environment Variables

The following environment variables can be set to configure the project:

- `NS3_DIR`: Path to your ns-3 installation (if not using the default)
- `MLPL_DATA_DIR`: Custom path for data storage
- `MLPL_RESULTS_DIR`: Custom path for results storage

You can set these in your shell profile or before running scripts:

```bash
export NS3_DIR=/path/to/ns-3
export MLPL_DATA_DIR=/path/to/data
```

## ns-3 Installation Guide 

### Installing ns-3 with Python Bindings

1. **Download ns-3**:
   ```bash
   git clone https://gitlab.com/nsnam/ns-3-dev.git
   cd ns-3-dev
   git checkout ns-3.36  # Or your desired version
   ```

2. **Configure with Python bindings**:
   ```bash
   ./waf configure --enable-examples --enable-tests --with-python=/usr/bin/python3
   ```

3. **Build**:
   ```bash
   ./waf build
   ```

4. **Update your PYTHONPATH**:
   
   Add the following to your `.bashrc` or `.zshrc`:
   ```bash
   export PYTHONPATH=$PYTHONPATH:/path/to/ns-3-dev/build/bindings/python
   ```
   
   On Windows, add to your environment variables or use:
   ```cmd
   set PYTHONPATH=%PYTHONPATH%;C:\path\to\ns-3-dev\build\bindings\python
   ```

### Verifying ns-3 Python Bindings

Run the following command to check if ns-3 Python bindings are correctly installed:

```bash
python -c "import ns.core; print('ns-3 Python bindings are working!')"
```

If you see "ns-3 Python bindings are working!", the installation is successful.

## Known Environment Issues and Solutions

### ns-3 Python Bindings Not Found

If you see errors importing ns-3 modules:

1. Ensure ns-3 is built with Python bindings (see above)
2. Check if the bindings path is in your PYTHONPATH
3. Try reinstalling ns-3 with the correct Python version

### GPU Setup for ML Training

For TensorFlow/PyTorch with GPU:

```bash
# Install GPU dependencies (CUDA, cuDNN)
# For TensorFlow:
pip install tensorflow-gpu

# For PyTorch with CUDA 11.6:
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu116
```

## Multiple Python Versions

If you need to use specific Python versions:

```bash
# Create virtual environment with specific Python version
python3.9 -m venv venv-py39

# Activate it
source venv-py39/bin/activate
```