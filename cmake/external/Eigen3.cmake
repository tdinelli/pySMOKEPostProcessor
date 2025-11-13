# -----------------------------------------------------------------------------
# FetchContent configuration for Eigen3
# -----------------------------------------------------------------------------
include(FetchContent)

message(STATUS "Configuring Eigen3...")

# -----------------------------------------------------------------------------
# Try to find system-installed Eigen3 first
find_package(Eigen3 3.3 QUIET NO_MODULE)

if(Eigen3_FOUND)
  message(STATUS "Using system-installed Eigen3 ${Eigen3_VERSION}")
else()
  message(STATUS "System Eigen3 not found, fetching from GitLab...")

  FetchContent_Declare(
    Eigen3
    GIT_REPOSITORY https://gitlab.com/libeigen/eigen.git
    GIT_TAG 3.4.0
    GIT_SHALLOW TRUE
    GIT_PROGRESS TRUE
  )

  FetchContent_MakeAvailable(Eigen3)

  message(STATUS "Eigen3 fetched successfully")
endif()
