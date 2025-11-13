# -----------------------------------------------------------------------------
# Preliminary Settings
# -----------------------------------------------------------------------------
cmake_minimum_required(VERSION 3.16)

project(pySMOKEPostProcessor
    VERSION 1.0.0
    DESCRIPTION "Python wrapper of the OpenSMOKEpp Graphical Post Processor"
    LANGUAGES CXX
)

# -----------------------------------------------------------------------------
# Set module path in order to use custom CMake modules
set(CMAKE_MODULE_PATH ${CMAKE_SOURCE_DIR}/cmake)

# -----------------------------------------------------------------------------
# C++ Standard
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

# -----------------------------------------------------------------------------
# Detect if building via scikit-build-core
if(DEFINED SKBUILD)
  message(STATUS "Building via scikit-build-core")
  set(SKBUILD_BUILD ON)
  # scikit-build sets installation directory
  set(CMAKE_INSTALL_PREFIX ${SKBUILD_PLATLIB_DIR}/pySMOKEPostProcessor)
else()
  message(STATUS "Building via standard CMake")
  set(SKBUILD_BUILD OFF)
  # For manual builds, install to project directory
  if(CMAKE_INSTALL_PREFIX_INITIALIZED_TO_DEFAULT)
    set(
      CMAKE_INSTALL_PREFIX "${PROJECT_SOURCE_DIR}/pySMOKEPostProcessor"
      CACHE PATH "Install prefix" FORCE
    )
  endif()
endif()

# -----------------------------------------------------------------------------
# Compulsory libraries
# -----------------------------------------------------------------------------
# Boost (Required by OpenSMOKEpp) Inside the installation to ease the life of
# everyone the boost package is installed using pip/conda pipeline
message(STATUS "Searching for Boost...")

# Set policy to use new FindBoost behavior (CMake 3.30+)
if(POLICY CMP0167)
  cmake_policy(SET CMP0167 NEW)
endif()

# Try to find Boost with modern config first (Boost 1.70+)
find_package(Boost 1.70 QUIET CONFIG)

if(NOT Boost_FOUND)
  # Fallback to FindBoost module for older versions
  find_package(Boost REQUIRED
      COMPONENTS
          date_time
          filesystem
          program_options
          system
          regex
          timer
          chrono
  )
endif()

if(Boost_FOUND)
  message(STATUS "Boost found: ${Boost_VERSION}")
  if(Boost_INCLUDE_DIRS)
    message(STATUS "Boost include: ${Boost_INCLUDE_DIRS}")
  elseif(Boost_INCLUDE_DIR)
    message(STATUS "Boost include: ${Boost_INCLUDE_DIR}")
  endif()
endif()

# -----------------------------------------------------------------------------
# External dependencies (FetchContent)
# -----------------------------------------------------------------------------
# Fetch Eigen3 (with system fallback)
include(cmake/external/Eigen3.cmake)

# -----------------------------------------------------------------------------
# Fetch pybind11 (with system fallback)
include(cmake/external/pybind11.cmake)

# -----------------------------------------------------------------------------
# Fetch OpenSMOKEpp v0.22
include(cmake/external/OpenSMOKEpp.cmake)

# -----------------------------------------------------------------------------
# Source code subdirectories
# -----------------------------------------------------------------------------
add_subdirectory(cxx_wrapper)
