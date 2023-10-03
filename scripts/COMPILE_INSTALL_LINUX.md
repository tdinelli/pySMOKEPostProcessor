# Installation guide

The installation is composed by the following steps:

1. Cloning this repository.
2. Check the availability of the OpenSMOKEpp library. (Now this is optional the project is setted up in a way that if you already have acces to the GitHub repository of OpenSMOKEpp the private one it will be added automatically).
3. Create the conda environment and run the installation script.
4. Install python package via "pip".

**N.B** Some of the commands here reported may change depending on the operating system you are using.

# 1. Cloning this repository

Clone this repository into your system
```bash
> git clone https://github.com/Titodinelli/pySMOKEPostProcessor
```

# 2. Check the availability of the OpenSMOKEpp library.

The pySMOKEPostProcessor is a binder in python for a c/c++ code so it directly have access to the shared library resulting from the built code exploiting [**ctypes**](https://docs.python.org/3/library/ctypes.html), a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries. It can be used to wrap these libraries in pure Python. In order to build the c interface to the core c++ code the following external libraries are needed:

- **OpenSMOKEpp** distibuted under request contact Alberto Cuoci <alberto.cuoci@polimi.it>
- **Eigen** (https://eigen.tuxfamily.org/index.php?title=Main_Page)
- **Boost** (https://www.boost.org/)

Eigen and Boost are automatically installed by creating the predefined conda environment, however the OpenSMOKEpp is distributed under request by A. Cuoci. If you already have access to the library in GitHub skip this part. In order to be able to compile the c++ interface of the post processor just set an environment variable pointing to the folder containing the source code of the library. In Linux this can be done as follow:
```bash
> export OpenSMOKEpp_ROOT=$my_path$
```

# 3. Create the conda environment and run the installation script.

Go into the base directory of the project, for instance the one containing the "setup.py" file. Run the following commands:
```bash
> conda env create -f environment-linux.yml
> conda activate post-processor
> cd scripts
> sh build-linux.sh
```

# 4. Install python package via "pip" 

Now that you have build and installed the shared library associated to the package you can install it via "pip". Run the following commands:

```bash
> python setup.py bdist_wheel
> pip install dist/pySMOKEPostProcessor-0.4.0-py3-none-any.whl
```

If everything worked fine something like this should be on your screen:

```bash
> Successfully installed pySMOKEPostProcessor-0.4.0
```
