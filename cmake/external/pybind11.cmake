# -----------------------------------------------------------------------------
# FetchContent configuration for pybind11
# -----------------------------------------------------------------------------
include(FetchContent)

message(STATUS "Configuring pybind11...")

# -----------------------------------------------------------------------------
# Try to find system-installed pybind11 first
find_package(pybind11 2.11.0 QUIET CONFIG)

if(pybind11_FOUND)
  message(STATUS "Using system-installed pybind11 ${pybind11_VERSION}")
else()
  message(STATUS "System pybind11 not found, fetching from GitHub...")

  FetchContent_Declare(
    pybind11
    GIT_REPOSITORY https://github.com/pybind/pybind11.git
    GIT_TAG v2.12.0
    GIT_SHALLOW TRUE
    GIT_PROGRESS TRUE
  )

  FetchContent_MakeAvailable(pybind11)

  message(STATUS "pybind11 fetched successfully")
endif()
