# Installation Guide

## Pre-built Wheels

Pre-built wheels are available on the [releases page](https://github.com/tdinelli/pySMOKEPostProcessor/releases).

```bash
# Download and install wheel for your platform
pip install pySMOKEPostProcessor-0.2.0-cp312-cp312-macosx_14_0_arm64.whl
```

Currently available:
- macOS ARM64 (M1/M2/M3) for Python 3.10, 3.11, 3.12
- Linux, Windows support planned

## Install from Source

### Prerequisites

C++ compiler and conda/mamba package manager.

### Steps

```bash
# Clone repository
git clone https://github.com/tdinelli/pySMOKEPostProcessor.git
cd pySMOKEPostProcessor

# Create and activate conda environment
conda env create -f environment.yml
conda activate pySMOKEPostProcessor

# Install package
pip install .          # For users
pip install -e .       # For developers (editable mode)
```

Build time: 2-5 minutes. The build system automatically:
1. Detects Boost and Eigen3 from conda
2. Fetches pybind11 and OpenSMOKEpp v0.22
3. Compiles C++ extension module

## Platform Setup

### Linux
```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

### macOS
```bash
xcode-select --install
```

### Windows
Install Visual Studio 2019+ with C++ support, or:
```bash
conda install cxx-compiler
```

## Verify Installation

```python
import pySMOKEPostProcessor
print("Installation successful!")
```

Run examples:
```bash
cd examples/python
python RateOfProductionAnalysis_1.py
```

## Troubleshooting

### Missing dependencies
```bash
conda install cmake        # CMake not found
conda install boost-cpp    # Boost not found
conda install eigen        # Eigen3 not found (usually auto-fetched)
conda install git          # For OpenSMOKEpp fetch
```

### Build issues
```bash
pip install . -vvv                           # Verbose output
pip install . --no-build-isolation -v        # Clean build
```

## Advanced

### Build wheels
```bash
pip install build
python -m build --wheel
# Output in dist/
```

### Uninstall
```bash
pip uninstall pySMOKEPostProcessor
conda deactivate
conda env remove -n pySMOKEPostProcessor
```

## Dependencies

### Auto-installed during build
- OpenSMOKEpp v0.22
- pybind11 ≥2.11
- Eigen3 ≥3.3

### Required (via conda)
- Python ≥3.8
- Boost ≥1.70
- CMake ≥3.16

### Python packages
- numpy ≥1.20
- pandas ≥1.3
- pyarrow ≥6.0
- matplotlib ≥3.3
- networkx ≥2.5
- pydot ≥1.4
- graphviz ≥0.16
- scipy ≥1.7

## Help

- Issues: https://github.com/tdinelli/pySMOKEPostProcessor/issues
- Examples: `examples/` directory
- Documentation: https://creckmodeling.chem.polimi.it/
