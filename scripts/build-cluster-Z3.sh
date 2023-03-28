#export Eigen3_ROOT="/software/chimica2/libraries/eigen/eigen-3.4.0"
#export Boost_ROOT="/software/chimica2/libraries/boost/boost-1.78.0-gcc-9.2.0"
#export CC=/software/chimica2/tools/gcc/gcc-9.2.0/bin/gcc
#export CXX=/software/chimica2/tools/gcc/gcc-9.2.0/bin/g++
export OpenSMOKEpp_ROOT="/home/chimica2/tdinelli/GitHub/OpenSMOKEpp"
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
cd ..
python setup.py bdist_wheel
pip install dist/pySMOKEPostProcessor-0.3.0-py3-none-any.whl
