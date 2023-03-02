#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEpostprocessor)
string(TOLOWER ${PROJECT_NAME} PROJECT_NAME_LOWER)
# --- Read version from the file
file(STRINGS "version" VERSION)

# --- Default configuration values
set(DEFAULT_BUILD_TYPE "Release")
set(DEFAULT_ARCH "x86-64")

# --- Detect platform
string(COMPARE EQUAL "Linux"   ${CMAKE_SYSTEM_NAME} LINUX)
string(COMPARE EQUAL "Windows" ${CMAKE_SYSTEM_NAME} WINDOWS)
string(COMPARE EQUAL "Darwin"  ${CMAKE_SYSTEM_NAME} OS_X)

if(LINUX)
    set(OS_STRING "linux")
elseif(WINDOWS)
    set(OS_STRING "windows")
elseif(OS_X)
    set(OS_STRING "osx")
else()
    set(OS_STRING "Unknown")
endif()

# --- Detect compiler
string(COMPARE EQUAL "Clang"      ${CMAKE_CXX_COMPILER_ID} CLANG)
string(COMPARE EQUAL "AppleClang" ${CMAKE_CXX_COMPILER_ID} APPLECLANG)
string(COMPARE EQUAL "GNU"        ${CMAKE_CXX_COMPILER_ID} GCC)
string(COMPARE EQUAL "Intel"      ${CMAKE_CXX_COMPILER_ID} INTEL)
string(COMPARE EQUAL "MSVC"       ${CMAKE_CXX_COMPILER_ID} MSVC)

if (CLANG OR APPLECLANG)
    set(CLANG 1)
endif()

# --- Set build type
if(NOT CMAKE_BUILD_TYPE)
    set(CMAKE_BUILD_TYPE ${DEFAULT_BUILD_TYPE})
endif()
message (STATUS "Compiling in mode: ${CMAKE_BUILD_TYPE}")

string(TOUPPER ${CMAKE_BUILD_TYPE} CMAKE_BUILD_TYPE)

# Set architecture to default if not set
if(NOT ARCH)
    set(ARCH ${DEFAULT_ARCH})
endif()

# Set bitness
if(${ARCH} STREQUAL "x86-64")
    set(BITNESS "64")
    set(BITNESS_FLAG "-m${BITNESS}")
elseif(${ARCH} STREQUAL "x86")
    set(BITNESS "32")
    set(BITNESS_FLAG "-m${BITNESS}")
elseif(${ARCH} STREQUAL "armv8")
    set(BITNESS "64")
    set(BITNESS_FLAG "")
elseif(${ARCH} STREQUAL "arm64")
    set(BITNESS "64")
    set(BITNESS_FLAG "")
else()
    set(BITNESS "32")
    set(ARCH "x86")
    set(BITNESS_FLAG "-m${BITNESS}")
    message("Unknown architecture selected, defaulting to x86")
endif()

# --- Set module path in order to use custom CMake modules
set (CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

set (CMAKE_CXX_STANDARD 14)
set (CMAKE_POSITION_INDEPENDENT_CODE ON)
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
# Set source and headers files
#--------------------------------------------------------------------

set ( C_INTERFACE_SOURCE_FILES
      ${CMAKE_SOURCE_DIR}/c_interface/c_interface.cpp
      ${CMAKE_SOURCE_DIR}/c_interface/c_utilities.cpp
)

set ( C_INTERFACE_INCLUDE_FILES
      ${CMAKE_SOURCE_DIR}/c_interface/c_interface.h
      ${CMAKE_SOURCE_DIR}/c_interface/c_utilities.h
      ${CMAKE_SOURCE_DIR}/c_interface/definitions.h
)

#--------------------------------------------------------------------
# Include flags
#--------------------------------------------------------------------

include_directories (${COMPULSORY_INCLUDE})

#--------------------------------------------------------------------
# Library flags
#--------------------------------------------------------------------

link_libraries (${COMPULSORY_LIBRARIES})

#--------------------------------------------------------------------
# Targets to compile
#--------------------------------------------------------------------

set(SHARED_LIBRARY ${PROJECT_NAME_LOWER}-${VERSION})

add_library(${SHARED_LIBRARY} SHARED
            ${C_INTERFACE_INCLUDE_FILES}
            ${C_INTERFACE_SOURCE_FILES}
)

#--------------------------------------------------------------------
# Installing options
#--------------------------------------------------------------------

#install(
#        DIRECTORY ${CMAKE_SOURCE_DIR}/pySMOKEPostProcessor
#        DESTINATION ${INSTALL_BIN_DIR}/python-postprocessor
#        PATTERN "*.pyc" EXCLUDE
#        PATTERN "__pycache__*" EXCLUDE
#)
#file(COPY ${CMAKE_SOURCE_DIR}/version DESTINATION ${INSTALL_BIN_DIR}/python-postprocessor/pySMOKEpostprocessor)
#install ( TARGETS ${SHARED_LIBRARY} 
#          DESTINATION ${INSTALL_BIN_DIR}/python-postprocessor/pySMOKEpostprocessor/lib/${OS_STRING}/${ARCH})

#--------------------------------------------------------------------
# Packing options
#--------------------------------------------------------------------

# TODO

message("Configuring ${PROJECT_NAME} version ${VERSION} in ${CMAKE_BUILD_TYPE} mode for ${ARCH} (${BITNESS} bit)")
message("Compiler flags: ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_${CMAKE_BUILD_TYPE}}")