# pySMOKEPostProcessor

[![Build Status](https://github.com/tdinelli/pySMOKEPostProcessor/actions/workflows/test.yml/badge.svg)](https://github.com/tdinelli/pySMOKEPostProcessor/actions/workflows/test.yml)
[![Release](https://github.com/tdinelli/pySMOKEPostProcessor/actions/workflows/wheels_cibuildwheel.yml/badge.svg)](https://github.com/tdinelli/pySMOKEPostProcessor/releases)

Python wrapper for the OpenSMOKEpp post processor computational core, developed by Professor [Alberto Cuoci](http://creckmodeling.chem.polimi.it/menu-people/menu-people-faculty/menu-people-alberto-cuoci). This version removes Qt5 dependencies and extends the capabilities of the [original C++ project](https://github.com/acuoci/OpenSMOKEppPostProcessor).

## Features

- Rate of Production Analysis
- Sensitivity Analysis and Coefficients
- Elementary Flux Analysis
- Reaction and Formation Rates
- Reaction Class Analysis

See [examples](examples) for notebooks and Python scripts.

## Installation

### Quick Start

```bash
# Create conda environment with dependencies
conda env create -f environment.yml
conda activate pySMOKEPostProcessor

# Install the package
pip install .
```

For detailed installation instructions, build options, and troubleshooting, see the [installation guide](doc/INSTALL.md).

## License

See the [LICENSE](LICENSE.md) file for license rights and limitations (GPL-3.0).
