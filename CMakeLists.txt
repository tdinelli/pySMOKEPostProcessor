#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEPostProcessor
    DESCRIPTION "Python binder of the OpenSMOKEpp Graphical Post Processor"
    LANGUAGES CXX)

set(DEFAULT_BUILD_TYPE "Release")
# --- Set build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE ${DEFAULT_BUILD_TYPE})
endif()
message (STATUS "Compiling in mode: ${CMAKE_BUILD_TYPE}")

# --- install location
set(CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor")
message(STATUS "Install location: ${CMAKE_INSTALL_PREFIX}")

# --- Set module path in order to use custom CMake modules
set (CMAKE_COLOR_MAKEFILE ON)
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 11)

set (CMAKE_POSITION_INDEPENDENT_CODE ON)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)

set (PROJECT_VERSION_MAJOR 0)
set (PROJECT_VERSION_MINOR 4)
set (PROJECT_VERSION_PATCH 0)
set (PROJECT_VERSION "${PROJECT_VERSION_MAJOR}.${PROJECT_VERSION_MINOR}.${PROJECT_VERSION_PATCH}")

#--------------------------------------------------------------------
# External modules
#--------------------------------------------------------------------

include(cmake/UpdateSubmodules.cmake)
add_subdirectory(external)

#--------------------------------------------------------------------
# Compulsory libraries
#--------------------------------------------------------------------

# --- Boost (Compulsory)
# set(Boost_USE_STATIC_LIBS   ON)
find_package (Boost REQUIRED COMPONENTS date_time filesystem program_options system regex timer chrono)
message (STATUS "Boost_INCLUDE_DIRS: ${Boost_INCLUDE_DIRS}")
message (STATUS "Boost_LIBRARIES: ${Boost_LIBRARIES}")

# --- Eigen (Compulsory)
find_package (Eigen3 REQUIRED)
message (STATUS "Eigen_LIBRARIES: ${EIGEN3_INCLUDE_DIR}")

# --- OpenSmoke++ (Compulsory)
find_package(OpenSMOKEpp REQUIRED)
message (STATUS "OpenSmoke++: ${OPENSMOKE_INCLUDE_DIR}")

# --- pybind11 (Compulsory)
# Uncomment if you want to provide your installation directory
# Just for distribution we will keep the things as easy as possible
# find_package(pybind11 REQUIRED)

set(COMPULSORY_LIBRARIES ${Boost_LIBRARIES})

set(COMPULSORY_INCLUDE ${Boost_INCLUDE_DIRS}
                       ${EIGEN3_INCLUDE_DIR}
                       ${OPENSMOKE_INCLUDE_DIR})

#--------------------------------------------------------------------
# Compilation flags and options
#--------------------------------------------------------------------

add_compile_options(-fPIC -m64 -w)
add_link_options(-fPIC -m64 -w)

#--------------------------------------------------------------------
# Targets to compile
#--------------------------------------------------------------------

pybind11_add_module(${PROJECT_NAME} ${PROJECT_SOURCE_DIR}/cpp_wrapper/PostProcessorWrapper_py.cpp)

target_include_directories(${PROJECT_NAME} 
    PRIVATE 
    ${PYBIND11_INCLUDE_DIRS} 
    ${PROJECT_SOURCE_DIR}/cpp_wrapper/source
    ${COMPULSORY_INCLUDE})

target_link_libraries(${PROJECT_NAME} 
    PRIVATE
    ${COMPULSORY_LIBRARIES}
    Eigen3::Eigen)

#--------------------------------------------------------------------
# Install directory
#--------------------------------------------------------------------

install(TARGETS ${PROJECT_NAME} 
    LIBRARY DESTINATION ${CMAKE_INSTALL_PREFIX})

#--------------------------------------------------------------------
# Packing options
#--------------------------------------------------------------------

# TODO
