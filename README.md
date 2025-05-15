# ns-3 + MLPL Research Project

## Overview
This repository contains research work combining ns-3 network simulator with Machine Learning in the Physical Layer (MLPL) techniques. The project aims to integrate modern ML approaches into network simulation to improve channel modeling, PHY layer performance, and overall network efficiency.

## Features
* ns-3 Integration: Custom modules and helpers for ns-3
* ML-Enhanced PHY Layer: Python-based ML models for channel prediction and optimization
* Modular Design: Reusable components for different research scenarios
* Comprehensive Documentation: API docs, user guides, and developer documentation
* Reproducible Experiments: Scripts and configurations for reproducing results

## Project Structure
```text
ns3-mlpl-research/
├── src/                    # Source code
│   ├── modules/           # ns-3 modules
│   ├── examples/          # Example applications
│   └── helper/            # Helper classes and utilities
├── docs/                  # Documentation
│   ├── api/              # API documentation
│   ├── user-guide/       # User guides and tutorials
│   └── developer-guide/  # Developer documentation
├── scripts/              # Build and utility scripts
│   ├── build/           # Build automation scripts
│   ├── experiments/     # Experiment execution scripts
│   └── analysis/        # Data analysis and plotting
├── data/                # Data files
│   ├── input/          # Input datasets
│   └── preprocessed/   # Processed data
├── results/             # Results and outputs
│   ├── experiments/    # Experiment results
│   ├── plots/         # Generated figures
│   └── logs/          # Execution logs
├── config/             # Configuration files
└── tests/              # Unit and integration tests
```

## Prerequisites
* ns-3 Simulator (version 3.x or later)
* Python (3.8 or later)
* Required Python packages (see requirements.txt)
* C++ Compiler (GCC or Clang)
* CMake (for building)

## Installation
1. Clone the repository:

```sh
git clone https://github.com/your-username/ns3-mlpl-research.git
cd ns3-mlpl-research
```

2. Set up Python environment:

```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Build the project:
```sh
./scripts/build/build.sh
```

## Quick Start
1. Run a basic example:
```sh
python src/examples/basic_mlpl_example.py
```

2. Execute a simulation:
```sh
./scripts/experiments/run_simulation.sh config/basic_config.yaml
```

3. Analyze results:
```sh
python scripts/analysis/analyze_results.py results/latest/
```

## Usage
### Running Simulations
To run a simulation with ML-enhanced PHY layer:

```sh
# Basic usage
python -m mlpl_sim --config config/simulation.yaml

# With custom parameters
python -m mlpl_sim --channels 10 --ml-model lstm --epochs 100
```

### Adding New ML Models
1. Create a new model class in `src/ml_models/`
2. Implement the required interface methods
3. Register the model in the model factory
4. Update configuration files as needed

### Extending ns-3 Modules
1. Add new C++ classes in `src/modules/`
2. Update the waf build configuration
3. Include Python bindings if needed
4. Add unit tests

## Configuration
Configuration files are stored in the `config/` directory. Key configuration files:

* `simulation.yaml`: Main simulation parameters
* `ml_config.yaml`: ML model configurations
* `channel_models.yaml`: Channel model parameters

## Results and Analysis
Results are automatically saved to `results/` with timestamps. Use the analysis scripts to:

* Generate performance plots
* Export data to various formats
* Create publication-ready figures

## Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Create a Pull Request

## Citation
If you use this work in your research, please cite:

```bibtex
@software{ns3_mlpl_research,
  title = {ns-3 + MLPL Research Framework},
  author = {Your Name and Contributors},
  year = {2025},
  url = {https://github.com/your-username/ns3-mlpl-research}
}
```

See CITATION.cff for more citation formats.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments
* ns-3 Project Team
* Machine Learning community
* Research collaborators and contributors

## Contact
* Primary Author: Lucas Mendes dpmendes@gmail.com
* Project Link: https://github.com/dpmendes/ns3-mlpl-research

## Changelog
### Version 0.1.0 (Initial Release)
* Basic project structure
* Initial ns-3 integration
* Example ML models for PHY layer
* Basic simulation framework
