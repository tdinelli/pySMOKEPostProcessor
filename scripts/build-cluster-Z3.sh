export Eigen3_ROOT="/software/chimica2/libraries/eigen/eigen-3.4.0"
export Boost_ROOT="/software/chimica2/libraries/boost/boost-1.78.0-gcc-9.2.0"
export OpenSMOKEpp_ROOT="/home/chimica2/tdinelli/GitHub/OpenSMOKEpp"
export CC=/software/chimica2/tools/gcc/gcc-9.2.0/bin/gcc
export CXX=/software/chimica2/tools/gcc/gcc-9.2.0/bin/g++
export ARCH=x86-64

# --- Do not modify below this
cd ..
rm -rf build
mkdir build
cd build
cmake \
    -DARCH=$ARCH \
    ..

make
make install
