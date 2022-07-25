# SET external libraries

export OPENSMOKE_INCLUDE_PATH=/home/chimica2/tdinelli/NumericalLibraries/opensmoke/OpenSMOKEpp/source
export EIGEN_INCLUDE_PATH=/software/chimica2/libraries/eigen/eigen-3.3.7
export BOOST_INCLUDE_PATH=/software/chimica2/libraries/boost/boost-1.78.0-gcc-9.2.0/include
export BOOST_LIBRARY_PATH=/software/chimica2/libraries/boost/boost-1.78.0-gcc-9.2.0/lib

# SET path to pySMOKEPostProcessor repository

export pySMOKEPostProcessor=/home/chimica2/tdinelli/GitHub/pySMOKEPostProcessor

# SET path where executable OpenSMOKEpp_RespecthConverter is saved

export TARGET_BIN=$pySMOKEPostProcessor/project/bin/Linux

# CHECKING THE EXISTENCE OF PROVIDED PATH

if [ ! -d $EIGEN_INCLUDE_PATH ]; then
	echo "$EIGEN_INCLUDE_PATH does not exist"
fi
if [ ! -d $BOOST_INCLUDE_PATH ]; then
	echo "$BOOST_INCLUDE_PATH does not exist"
fi
if [ ! -d $BOOST_LIBRARY_PATH ]; then
	echo "$BOOST_LIBRARY_PATH does not exist"
fi
if [ ! -d $OPENSMOKE_INCLUDE_PATH ]; then
	echo "$OPENSMOKE_INCLUDE_PATH does not exist"
fi 
if [ ! -d $CurveMatchingROOT ]; then
	echo "$CurveMatchingROOT does not exist"
fi
if [ ! -d $TARGET_BIN ]; then
	echo "$TARGET_BIN does not exist"
fi

echo "Building pySMOKEPostProcessor binaries (...)"

g++ \
    -w \
    -O3 \
    -lpq \
    -pthread \
    -fPIC \
    -shared \
    -std=c++17 \
    -I$OPENSMOKE_INCLUDE_PATH \
    -I$EIGEN_INCLUDE_PATH \
    -I$BOOST_INCLUDE_PATH \
    -L$BOOST_LIBRARY_PATH \
    -lboost_date_time \
    -lboost_filesystem \
    -lboost_system \
    -lboost_regex \
    -lboost_program_options \
    -lboost_json \
    -lboost_atomic \
    -lboost_container \
    $pySMOKEPostProcessor/source/*.cpp \
    -o $TARGET_BIN/pySMOKEPostProcessor.o

echo "Done!"
