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
