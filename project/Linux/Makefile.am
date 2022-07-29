AUTOMAKE_OPTIONS = foreign

if INTEL_COMPILER
AM_CXXFLAGS = -O3 -m64 -fPIC -std=c++11 @OPENMP_INTEL@
else
AM_CXXFLAGS = -O3 -m64 -fPIC -std=c++11 @OPENMP_GNU@
endif

AM_CPPFLAGS = 	@COMPULSORY_INCLUDE_DIRS@ 
AM_LDFLAGS  =   

#List of programs
bin_PROGRAMS = 	pySMOKEPostProcessor.sh

pySMOKEPostProcessor_sh_SOURCES = ../../pySMOKEPostProcessor/source/main.cpp
pySMOKEPostProcessor_sh_LDADD = @BOOST_LIBS@ -lgfortran 
