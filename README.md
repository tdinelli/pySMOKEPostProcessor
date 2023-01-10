# pySMOKEPostProcessor

Python binder for the OpenSMOKEpp Graphical PostProcessor developed by Professor [Alberto Cuoci](http://creckmodeling.chem.polimi.it/menu-people/menu-people-faculty/menu-people-alberto-cuoci). You can find the original repository of the OpenSMOKE PostProcessor at this link (https://github.com/acuoci/OpenSMOKEppPostProcessor).

## External libraries dependencies

- OpenSMOKEpp distibuted under request contact Alberto Cuoci <alberto.cuoci@polimi.it>
- Eigen (https://eigen.tuxfamily.org/index.php?title=Main_Page)
- Boost (https://www.boost.org/)

## External python packages dependencies

- pydot
- graphviz 
- ctypes
- Element Tree
- networkx
- pandas

Just to run the [examples](examples/)

- numpy
- matplotlib
## Compile

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
make install
```
In order to make CMAKE able to find the necessary libraries it is recommended to set the following environment variables:

- export Boost_ROOT  = $ PATH_TO_YOUR_BOOST_INSTALLATION
- export Eigen3_ROOT = $ PATH_TO_YOUR_EIGEN_INSTALLATION
- export OpenSMOKEpp_ROOT = $ PATH_TO_YOUR_OPENSMOKE_INSTALLATION
## Installing

```bash
python setup.py install
```

## Features

- **Rate Of Production Analysis**
- **Sensitivity Analysis**
- **Flux Analysis**
- **Reaction Rates plots**: TODO
- **Sensitivity Coefficients plots**: TODO
- **Adaption to ROPA reaction class post processing**: (ALMOST)

## Examples
