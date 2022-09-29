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

Just to run the [examples](examples/)

- pandas
- numpy
- matplotlib
## Installing 

**N.B.** At the moment the package is tested only in Linux however soon there will be also a detailed procedure also for Windows and MacOS.

Clone this repository into your system
```bash
git clone https://github.com/Titodinelli/pySMOKEPostProcessor
```
After the cloning edit the file named preconfigure.sh inside the folder [**project/Linux**](project/Linux/) adding the required paths to the necessary libraries. And run the following commands paying attention to remain into the same folder:

```bash
sh preconfigure.sh
make
make install
```
## Install with pip

```bash
python setup.py bdist_wheel
```
```bash
pip install dist/pySMOKEPostProcessor-0.1.0-py3-none-any.whl
```

## Features

- **Rate Of Production Analysis**
- **Sensitivity Analysis**
- **Flux Analysis**
- **Reaction Rates plots**: TODO
- **Sensitivity Coefficients plots**: TODO
- **Adaption to ROPA reaction class post processing**: TODO
- **Stoichiometric map**: WIP
- **Enabling PostProcessing after @OnTheFlyPostProcessing**
- **Association between reaction name and index inside the kinetic scheme**

## Examples
