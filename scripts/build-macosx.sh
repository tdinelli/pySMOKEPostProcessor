export Eigen3_ROOT="/Users/tdinelli/NumericalLibraries/eigen/eigen-3.4.0"
export Boost_ROOT="/Users/tdinelli/NumericalLibraries/boost/boost-1.79-gcc-12"
export OpenSMOKEpp_ROOT="/Users/tdinelli/Documents/GitHub/OpenSMOKEpp"
export CC=/opt/homebrew/bin/gcc-12
export CXX=/opt/homebrew/bin/g++-12
export ARCH=arm64
# --- Do not modify below this
cd ..
rm -rf build
mkdir build
cd build
cmake \
    -DARCH=$ARCH\
    ..

make
make install