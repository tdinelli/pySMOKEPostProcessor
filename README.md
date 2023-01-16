# pySMOKEPostProcessor

Python binder for the OpenSMOKEpp Graphical PostProcessor developed by Professor [Alberto Cuoci](http://creckmodeling.chem.polimi.it/menu-people/menu-people-faculty/menu-people-alberto-cuoci). You can find the original repository of the OpenSMOKE PostProcessor at this link (https://github.com/acuoci/OpenSMOKEppPostProcessor).

## External libraries dependencies

- OpenSMOKEpp distibuted under request contact Alberto Cuoci <alberto.cuoci@polimi.it>
- Eigen (https://eigen.tuxfamily.org/index.php?title=Main_Page)
- Boost (https://www.boost.org/)

## Compile and Install

**N.B.** At the moment the package is tested only in Linux and MacOS however soon there will be also a detailed procedure also for Windows.

Clone this repository into your system
```bash
git clone https://github.com/Titodinelli/pySMOKEPostProcessor
```
Inside the base path of the repository (the one that contains the CMakeLists.txt file) run the following commands (note that they can change depending on the operative system): 

```bash
mkdir build
cd build
cmake ..
make
```
In order to make CMAKE able to find the necessary libraries it is recommended to set the following environment variables:

- export Boost_ROOT  = $ PATH_TO_YOUR_BOOST_INSTALLATION
- export EIGEN3_ROOT = $ PATH_TO_YOUR_EIGEN_INSTALLATION
- export OpenSMOKEpp_ROOT = $ PATH_TO_YOUR_OPENSMOKE_INSTALLATION

Once the compilation is done whithin your package manager run the following command.
```bash
python setup.py install
```

## Features

- **Rate Of Production Analysis**
- **Sensitivity Analysis**
- **Elementary Flux Analysis**
- **Reaction Rates plots**
- **Formation Rates plots**
- **Sensitivity Coefficients plots**
- **Rate Of Production Analysis for reaction classes**

## WIP

- Characteristic Times analysis
- Plot of the shortest time scale
