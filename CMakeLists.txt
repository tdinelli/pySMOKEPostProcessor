#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEPostProcessor)

set(DEFAULT_BUILD_TYPE "Release")

# --- Set build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE ${DEFAULT_BUILD_TYPE})
endif()
message (STATUS "Compiling in mode: ${CMAKE_BUILD_TYPE}")

string(TOUPPER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE)

# --- Set module path in order to use custom CMake modules
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 17)
set (CMAKE_POSITION_INDEPENDENT_CODE ON)
set (CMAKE_EXPORT_COMPILE_COMMANDS ON)
set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} $ENV{EIGEN_LIBRARY_PATH}/cmake)
set (CMAKE_COLOR_MAKEFILE ON)
set (PROJECT_VERSION_MAJOR 0)
set (PROJECT_VERSION_MINOR 3)
set (PROJECT_VERSION_PATCH 0)
set (INSTALL_BIN_DIR "${CMAKE_INSTALL_PREFIX}" CACHE PATH "Installation directory for executables")

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

# --- pybind11 (Compulsory)
find_package(pybind11 REQUIRED)

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
# Targets to compile
#--------------------------------------------------------------------

pybind11_add_module(${PROJECT_NAME} ${PROJECT_SOURCE_DIR}/cpp_wrapper/PostProcessorWrapper_py.cpp)

#target_compile_definitions(${PROJECT_NAME})# PRIVATE VERSION_INFO=${EXAMPLE_VERSION_INFO})

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

# install(${PROJECT_NAME} DESTINATION ${CMAKE_INSTALL_PREFIX})

#--------------------------------------------------------------------
# Packing options
#--------------------------------------------------------------------

# TODO
