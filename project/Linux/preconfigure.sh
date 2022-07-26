aclocal
automake --add-missing
autoconf
./configure \
CXX=g++ \
--enable-openmp=no \
--prefix=$HOME/Documents/GitHub/pySMOKEPostProcessorNEW/projects/Linux-lib \
--with-opensmoke=$HOME/Documents/GitHub/OpenSMOKEpp \
--with-eigen=$HOME/libraries/eigen/eigen-3.4.0/include/eigen3 \
--with-boost-include=$HOME/libraries/boost/boost-1.71-gcc-9.4/include \
--with-boost-lib=$HOME/libraries/boost/boost-1.71-gcc-9.4/lib \
