export Eigen3_ROOT="/Users/tdinelli/NumericalLibraries/eigen/eigen-3.4.0"
export Boost_ROOT="/Users/tdinelli/NumericalLibraries/boost/boost-1.79-gcc-12"
export OpenSMOKEpp_ROOT="/Users/tdinelli/Documents/GitHub/OpenSMOKEpp"

cd ..
rm -rf build
mkdir build
cd build
cmake \
    -DCMAKE_C_COMPILER=/opt/homebrew/bin/gcc-12 \
    -DCMAKE_CXX_COMPILER=/opt/homebrew/bin/g++-12 \
    -DARCH=arm64 \
    -DCMAKE_INSTALL_PREFIX=/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/pySMOKEPostProcessor/lib/osx/arm64 \
    ..

make
