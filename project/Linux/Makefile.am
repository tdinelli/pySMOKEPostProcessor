AUTOMAKE_OPTIONS = foreign

if INTEL_COMPILER
AM_CXXFLAGS = -O3 -m64 -fPIC -shared -std=c++11 @OPENMP_INTEL@
else
AM_CXXFLAGS = -O3 -m64 -fPIC -shared -std=c++11 @OPENMP_GNU@
endif

AM_CPPFLAGS = 	@COMPULSORY_INCLUDE_DIRS@ 
AM_LDFLAGS  =   
#List of programs
bin_PROGRAMS = 	pySMOKEPostProcessor.o

pySMOKEPostProcessor_o_SOURCES = ../../pySMOKEPostProcessor/source/main.cpp
pySMOKEPostProcessor_o_LDADD = @BOOST_LIBS@ -lgfortran 
