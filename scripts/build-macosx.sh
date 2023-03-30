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
cd ..
python setup.py bdist_wheel
pip install dist/pySMOKEPostProcessor-0.3.0-py3-none-any.whl
