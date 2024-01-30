#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEPostProcessor
    DESCRIPTION
    "Python interface of the OpenSMOKEpp Graphical Post Processor"
    LANGUAGES
    CXX
)


# --- install location
# Not super sure about this
set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor")
message(STATUS "Install location: ${CMAKE_INSTALL_PREFIX}")

# --- Set module path in order to use custom CMake modules
set (CMAKE_COLOR_MAKEFILE ON)
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 14)

set (CMAKE_POSITION_INDEPENDENT_CODE ON)

set (PROJECT_VERSION_MAJOR 1)
set (PROJECT_VERSION_MINOR 0)
set (PROJECT_VERSION_PATCH 0)
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

#--------------------------------------------------------------------
# Compulsory libraries
#--------------------------------------------------------------------

# --- Boost (Compulsory required by OpenSMOKEpp)
find_package (Boost
    REQUIRED
    COMPONENTS
    date_time
    filesystem
    program_options
    system
    regex
    timer
    chrono
)

# --- Eigen (Compulsory rquired by OpenSMOKEpp)
find_package (Eigen3 REQUIRED)

#--------------------------------------------------------------------
# External submodules
#--------------------------------------------------------------------

# Note: pyBIND11 and OpenSMOKEpp are included as submodules in order
# to ease the installation of the python package
include(cmake/UpdateSubmodules.cmake)
add_subdirectory(external)

# --- OpenSMOKEpp: We are using submodules just to handle the cloning
find_package(OpenSMOKEpp REQUIRED)

#--------------------------------------------------------------------
# Source code subdirectories
#--------------------------------------------------------------------

add_subdirectory(cxx_wrapper)
