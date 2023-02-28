#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEpostprocessor)

# --- Set module path in order to use custom CMake modules
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 14)
set (CMAKE_POSITION_INDEPENDENT_CODE ON)
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} $ENV{EIGEN_LIBRARY_PATH}/cmake)
set (CMAKE_COLOR_MAKEFILE ON)
set (VERSION "0.3.0")
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
message (STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
message (STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")

# --- Eigen (Compulsory)
find_package (Eigen3 REQUIRED)
message (STATUS "Eigen_LIBRARIES: ${EIGEN3_INCLUDE_DIR}")

# --- OpenSmoke++ (Compulsory)
find_package(OpenSMOKEpp REQUIRED)
message (STATUS "OpenSmoke++: ${OpenSMOKEpp_INCLUDE_DIR}")

set(COMPULSORY_LIBRARIES ${Boost_LIBRARIES})

set(COMPULSORY_INCLUDE ${Boost_INCLUDE_DIRS}
                       ${EIGEN3_INCLUDE_DIR}
                       ${OpenSMOKEpp_INCLUDE_DIR})
#--------------------------------------------------------------------
# Compilation flags and options
#--------------------------------------------------------------------

add_compile_options(-fPIC -m64 -w)
add_link_options(-fPIC -m64 -w)

#--------------------------------------------------------------------
# Include flags
#--------------------------------------------------------------------

include_directories (${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor/c_interface
                     ${COMPULSORY_INCLUDE})
#--------------------------------------------------------------------
# Library flags
#--------------------------------------------------------------------

link_libraries (${COMPULSORY_LIBRARIES})

#--------------------------------------------------------------------
# Set source and headers files
#--------------------------------------------------------------------

set ( CPP_SOURCE_FILES 
  pySMOKEPostProcessor/c_interface/source/utilities.cpp
)

set (CPP_INCLUDE
  pySMOKEPostProcessor/c_interface/source/utilities.h
)

set ( C_INTERFACE_SOURCE_FILES
  pySMOKEPostProcessor/c_interface/c_interface.cpp
  pySMOKEPostProcessor/c_interface/c_utilities.cpp
)

set ( C_INTERFACE_INCLUDE_FILES
  pySMOKEPostProcessor/c_interface/c_interface.h
  pySMOKEPostProcessor/c_interface/c_utilities.h
  pySMOKEPostProcessor/c_interface/definitions.h
)

#--------------------------------------------------------------------
# Targets to compile
#--------------------------------------------------------------------

add_library(pySMOKEPostProcessor SHARED
            ${CPP_SOURCE_FILES}
            ${CPP_INCLUDE}
)

#--------------------------------------------------------------------
# Installing options
#--------------------------------------------------------------------
