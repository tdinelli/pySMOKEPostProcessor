
SOURCE=""
TARGETBIN=""
OPENSMOKE="/Users/edoardo/Desktop/source"
EIGEN="/usr/local/include/eigen3"
BOOST_LIB="/usr/local/Cellar/boost/1.78.0/lib"
BOOST_INC="/usr/local/Cellar/boost/1.78.0/include"

g++ \
	--std=c++17 \
	-I $EIGEN \
	-I $BOOST_INC \
	-I $OPENSMOKE \
	-L $BOOST_LIB \
	-lboost_filesystem \
	$SOURCE/main.cpp \
	-o $TARGETBIN/pySMOKEPostProcessor.o \
	-O3 \
	-Wall \
	-DNDEBUG \
	-fPIC \
	-w \

