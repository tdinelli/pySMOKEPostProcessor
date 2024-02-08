add_subdirectory(pybind11)

set(OPENSMOKE_INCLUDE
    ${CMAKE_CURRENT_LIST_DIR}/opensmoke/source
    CACHE
    PATH
    "Path to OpenSMOKE library"
)
