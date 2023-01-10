#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEpostprocessor)

# --- Set module path in order to use custom CMake modules
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 17)
set (CMAKE_POSITION_INDEPENDENT_CODE ON)
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} $ENV{EIGEN_LIBRARY_PATH}/cmake)
set (CMAKE_COLOR_MAKEFILE ON)
set (VERSION "0.2.0")
set (INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}/bin" CACHE PATH "Installation directory for executables")

if( NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE Release)
endif()

message (STATUS "Compiling in mode: ${CMAKE_BUILD_TYPE}")

#--------------------------------------------------------------------
# Compulsory libraries
#--------------------------------------------------------------------

# --- Boost (Compulsory)
find_package (Boost REQUIRED COMPONENTS date_time filesystem program_options system regex timer chrono)
message (STATUS "Boost_INCLUDE_DIRS = ${Boost_INCLUDE_DIRS}")
message (STATUS "Boost_LIBRARIES    = ${Boost_LIBRARIES}")

# --- Eigen (Compulsory)
find_package (Eigen3 REQUIRED)
message (STATUS "Eigen_LIBRARIES = ${EIGEN3_INCLUDE_DIR}")

# --- OpenSmoke++ (Compulsory)
find_package(OpenSMOKEpp REQUIRED)
message (STATUS "OpenSmoke++        = ${OpenSMOKEpp_INCLUDE_DIR}")

set(COMPULSORY_LIBRARIES ${Boost_LIBRARIES})

set(COMPULSORY_INCLUDE ${Boost_INCLUDE_DIRS}
                       ${EIGEN3_INCLUDE_DIR}
                       ${OpenSMOKEpp_INCLUDE_DIR})
#--------------------------------------------------------------------
# Compilation flags and options
#--------------------------------------------------------------------

# Suppress warnings
option(OPENSMOKE_USE_OPENMP "Activate support for OpenMP" FALSE)
if (OPENSMOKE_USE_OPENMP)
  add_compile_options(-fopenmp)
  add_link_options(-fopenmp)
endif()

add_compile_options(-std=c++17 -fPIC -m64 -w -shared -lgfortran)
add_link_options(-std=c++17 -fPIC -m64 -w -shared -lgfortran)

#--------------------------------------------------------------------
# Include flags
#--------------------------------------------------------------------

INCLUDE_DIRECTORIES (${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor/source
                     ${COMPULSORY_INCLUDE})
#--------------------------------------------------------------------
# Library flags
#--------------------------------------------------------------------

LINK_LIBRARIES (${COMPULSORY_LIBRARIES})
#--------------------------------------------------------------------
# Targets to compile
#--------------------------------------------------------------------

add_executable (pySMOKEPostProcessor.o pySMOKEPostProcessor/source/main.cpp)

#--------------------------------------------------------------------
# Installing options
#--------------------------------------------------------------------
