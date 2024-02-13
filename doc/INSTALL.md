# Installation guide

The installation is composed by the following steps:

1. Cloning this repository.
2. Create the conda environment to automatically manage the dependencies.
3. Install python package via "pip".

**N.B** Some of the commands here reported may change depending on the operating system you are using.

## 1. Cloning this repository

Clone this repository into your system.

```bash
> git clone https://github.com/Titodinelli/pySMOKEPostProcessor
```

## 2. Create the conda environment.

This is step is in principle optional, however it is strongly recommended unless you do not really know what you are doing. The package rely on an interfaced wrapper between a C++ code and python. Thus the project, has the following dependencies.

- **OpenSMOKEpp** distibuted under request contact Alberto Cuoci <alberto.cuoci@polimi.it>, within the project this dependency is automatically handled as a sub-module by cmake and git, just be sure to have access to the GitHub repository.
- **Eigen** (https://eigen.tuxfamily.org/index.php?title=Main_Page), handled by conda.
- **Boost** (https://www.boost.org/), handled by conda.
- **pybind11** (https://pybind11.readthedocs.io/en/stable/), handled as a sub-module by cmake and git.

Go into the [conda.recipe](conda.recipe) directory, and run the following commands:

```bash
> conda env create -f environment-linux.yaml
```

## 3. Install python package via "pip" 
Work from the base folder pySMOKEPostProcessor.
```bash
> conda activate pp
> source export_var.sh
> python -m pip install .
```

If everything worked fine something like this should be on your screen:

```bash
> Successfully installed pySMOKEPostProcessor-0.3.0
```

## Development functionalities

Way of controlling the installation procedure of the package run the pip install command in verbose mode:
```bash
> python -m pip install . -vvv
``` 

In order to update the package after changing source code files.
```bash
> python -m pip install . -U
``` 
