# --------------------------------------------------------------------
# Preliminary Settings
# --------------------------------------------------------------------
cmake_minimum_required(VERSION 3.16)

project(
  pySMOKEPostProcessor
  DESCRIPTION "Python wrapper of the OpenSMOKEpp Graphical Post Processor"
  VERSION 2.0.0
  LANGUAGES CXX)

# install location Not super sure about this
set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor")

# Set module path in order to use custom CMake modules
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")
set(CMAKE_CXX_STANDARD 17)

# --------------------------------------------------------------------
# Compulsory libraries
# --------------------------------------------------------------------

# Boost (Compulsory required by OpenSMOKEpp)
find_package(
  Boost REQUIRED
  COMPONENTS date_time
             filesystem
             program_options
             system
             regex
             timer
             chrono)

# Eigen (Compulsory rquired by OpenSMOKEpp)
find_package(Eigen3 REQUIRED)

# --------------------------------------------------------------------
# External submodules
# --------------------------------------------------------------------

# Note: pyBIND11 and OpenSMOKEpp are included as submodules in order to ease the
# installation of the python package
include(cmake/UpdateSubmodules.cmake)
add_subdirectory(external)

# --------------------------------------------------------------------
# Source code subdirectories
# --------------------------------------------------------------------

add_subdirectory("${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor/cxx_wrapper")
