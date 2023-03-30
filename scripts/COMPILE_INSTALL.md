# Installation guide

The installation is composed by the following steps:

1. Cloning this repository
2. Checking the availability of the external dependecies.
3. Running one of the scripts provided to  build the c/c++ interface
4. Install python package via "pip"

**N.B.** At the moment the package is tested only in Linux and MacOS however soon there will be also a detailed procedure also for Windows.

**N.B.2** Some of the commands here reported may change depending on the operating system you are using.

# 1. Cloning this repository

Clone this repository into your system
```bash
> git clone https://github.com/Titodinelli/pySMOKEPostProcessor
```
# 2. Check the availability of the external dependecies.

The pySMOKEPostProcessor is a binder in python for a c/c++ code so it directly have access to the shared library resulting from the built code exploiting [**ctypes**](https://docs.python.org/3/library/ctypes.html), a foreign function library for Python. It provides C compatible data types, and allows calling functions in DLLs or shared libraries. It can be used to wrap these libraries in pure Python. In order to build the c interface to the core c++ code the following external libraries are needed:

- **OpenSMOKEpp** distibuted under request contact Alberto Cuoci <alberto.cuoci@polimi.it>
- **Eigen** (https://eigen.tuxfamily.org/index.php?title=Main_Page)
- **Boost** (https://www.boost.org/)

# 3. Building c-interface
Inside the folder [scripts](scripts) there are some bash scripts to perform the automatic built of the c-interface. The user have just to set the directories of installation for the external libraries and optionally the path for the different compilers. In the case that some of the external dependencies have been installed with some package managers just comment the line and CMake will try to locate them for you. The same thing is valid for the variable *ARCH* you don't know your pc architecture CMake will try to understand it by itself.

**N.B.** Do not change the install prefix of the library unless it is strictly necessary, or you know what you are doing. Because the program is wirtten in order to automatically locate the shared library and won't look into non standard locations.

```bash
> cd scripts
> sh build-**.sh
```

In order to be sure that the built has been performed correctly you shuold see something like that on the screen:

```
[100%] Built target pysmokepostprocessor-0.3.0
Install the project...
-- Install configuration: "RELEASE"
-- Installing: /Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/pySMOKEPostProcessor/lib/osx/arm64/libpysmokepostprocessor-0.3.0.dylib
```

# 4. Install python package via "pip" 

Now that you have build and installed the shared library associated to the package you can install it via "pip". Run the following commands:

```bash
> python setup.py bdist_wheel
> pip install dist/pySMOKEPostProcessor-0.3.0-py3-none-any.whl
```

If everything worked fine something like this should be on your screen:

```bash
> Successfully installed pySMOKEPostProcessor-0.3.0
```
