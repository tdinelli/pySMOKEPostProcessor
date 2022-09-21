aclocal
automake --add-missing
autoconf
./configure \
CXX=clang++ \
--prefix=$HOME/Documents/GitHub/pySMOKEPostProcessor/project/Linux-exe \
--with-opensmoke=$HOME/Documents/GitHub/OpenSMOKEpp \
--with-eigen=$HOME/NumericalLibraries/eigen/eigen-3.4.0/ \
--with-boost-include=$HOME/NumericalLibraries/boost/boost-1.80-clang/include \
--with-boost-lib=$HOME/NumericalLibraries/boost/boost-1.80-clang/lib \
