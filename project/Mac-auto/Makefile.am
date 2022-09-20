# AUTOMAKE_OPTIONS = foreign

#if GNU_COMPILER
#AM_CXXFLAGS = -O3 -m64 -fPIC -shared -std=c++11
#else
AM_CXXFLAGS = -O3 -m64 -fPIC -shared -std=c++11
#endif

AUTOMAKE_OPTIONS = subdir-objects
AM_CPPFLAGS = 	@COMPULSORY_INCLUDE_DIRS@ 
AM_LDFLAGS  = @BOOST_LIBS@
#List of programs
bin_PROGRAMS = 	pySMOKEPostProcessor.o

pySMOKEPostProcessor_o_SOURCES = ../../pySMOKEPostProcessor/source/main.cpp
pySMOKEPostProcessor_o_LDADD =
