# -----------------------------------------------------------------------------
# FetchContent configuration for OpenSMOKEpp
# -----------------------------------------------------------------------------
include(FetchContent)

message(STATUS "Configuring OpenSMOKEpp...")

# -----------------------------------------------------------------------------
# OpenSMOKEpp is a header-only library, we just need to fetch it
FetchContent_Declare(
  opensmoke
  GIT_REPOSITORY https://github.com/acuoci/OpenSMOKEpp.git
  GIT_TAG v0.22
  GIT_SHALLOW TRUE
  GIT_PROGRESS TRUE
  SOURCE_DIR ${CMAKE_CURRENT_BINARY_DIR}/_deps/opensmoke-src
)

FetchContent_MakeAvailable(opensmoke)

# Set the include path for OpenSMOKEpp
set(OPENSMOKE_INCLUDE
  ${opensmoke_SOURCE_DIR}/source
  CACHE PATH "Path to OpenSMOKE library"
)

message(STATUS "OpenSMOKEpp v0.22 fetched successfully")
message(STATUS "OpenSMOKEpp include path: ${OPENSMOKE_INCLUDE}")
