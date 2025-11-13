# Installation Guide for pySMOKEPostProcessor

This guide provides instructions for installing pySMOKEPostProcessor from pre-built packages or from source.

---

## Quick Installation (Recommended)

### Option 1: Install from pre-built wheels

Pre-built wheels are automatically generated for each release and are available on the [GitHub Releases page](https://github.com/tdinelli/pySMOKEPostProcessor/releases).

#### Download and install a wheel:

```bash
# Download the wheel for your platform and Python version from the latest release
# Example for macOS ARM64 with Python 3.12:
pip install pySMOKEPostProcessor-0.2.0-cp312-cp312-macosx_14_0_arm64.whl
```

**Currently available platforms:**
- macOS ARM64 (Apple Silicon M1/M2/M3) for Python 3.10, 3.11, 3.12

**Note**: Additional platforms (Linux, Windows) may be added in future releases.

---

## Installation from Source

### Prerequisites

You need a C++ compiler and conda/mamba package manager.

### Step 1: Create a conda environment

Create and activate a new conda environment with all required dependencies:

```bash
# Clone the repository
git clone https://github.com/tdinelli/pySMOKEPostProcessor.git
cd pySMOKEPostProcessor

# Create conda environment from environment.yml
conda env create -f environment.yml

# Activate the environment
conda activate pySMOKEPostProcessor
```

### Step 2: Install the package

#### For users (install mode):

```bash
pip install .
```

#### For developers (editable mode):

```bash
pip install -e .
```

The `-e` flag installs in editable mode, so changes to Python files take effect immediately.

---

## What happens during installation?

The build system will automatically:

1. Detect Boost and Eigen3 from conda environment
2. Fetch pybind11 (if not found in system)
3. Fetch OpenSMOKEpp v0.22 from GitHub
4. Compile the C++ extension module
5. Install the Python package

Build time: ~2-5 minutes (depending on your machine)

---

## Platform-Specific Notes

### Linux

Ensure you have a C++ compiler:

```bash
# Ubuntu/Debian
sudo apt-get install build-essential

# CentOS/RHEL
sudo yum groupinstall "Development Tools"
```

### macOS

Install Xcode Command Line Tools:

```bash
xcode-select --install
```

### Windows

Install Visual Studio 2019 or later with C++ support, or use conda-provided compilers:

```bash
conda install cxx-compiler
```

---

## Verifying the Installation

Test your installation:

```python
import pySMOKEPostProcessor
print("Installation successful!")
```

Run the examples:

```bash
# Navigate to examples
cd examples/python

# Run a sample script
python RateOfProductionAnalysis_1.py
```

---

## Troubleshooting

### CMake not found

```bash
conda install cmake
```

### Boost not found

```bash
conda install boost-cpp
```

### Eigen3 not found

Eigen3 should be fetched automatically, but you can install it via conda:

```bash
conda install eigen
```

### Build fails with "OpenSMOKEpp not found"

The build system should fetch OpenSMOKEpp automatically. If it fails:

1. Check your internet connection
2. Ensure you have git installed: `conda install git`
3. Try cleaning the build: `pip install . --no-build-isolation -v`

### Verbose build output

For debugging build issues:

```bash
pip install . -vvv
```

---

## Advanced: Building wheels for distribution

To build distributable wheels:

```bash
# Install build tools
pip install build

# Build wheel
python -m build --wheel

# Wheel will be in dist/
```

---

## Uninstalling

```bash
pip uninstall pySMOKEPostProcessor
```

To also remove the conda environment:

```bash
conda deactivate
conda env remove -n pySMOKEPostProcessor
```

---

## Dependencies Summary

### Required (automatically installed):
- **OpenSMOKEpp v0.22**: Fetched from GitHub during build
- **pybind11 ≥2.11**: Fetched if not found
- **Eigen3 ≥3.3**: Fetched if not found

### Required (must be installed):
- **Python ≥3.8**
- **Boost ≥1.70**: Install via conda (`conda install boost-cpp`)
- **CMake ≥3.16**: Install via conda (`conda install cmake`)

### Python packages:
- numpy ≥1.20
- pandas ≥1.3
- pyarrow ≥6.0
- matplotlib ≥3.3
- networkx ≥2.5
- pydot ≥1.4
- graphviz ≥0.16
- scipy ≥1.7

---

## Getting Help

- **Issues**: https://github.com/tdinelli/pySMOKEPostProcessor/issues
- **Examples**: See the `examples/` directory
- **Documentation**: https://creckmodeling.chem.polimi.it/
