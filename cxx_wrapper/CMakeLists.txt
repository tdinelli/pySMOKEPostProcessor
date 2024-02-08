pybind11_add_module(${PROJECT_NAME}
    ${CMAKE_CURRENT_LIST_DIR}/PostProcessorWrapper_py.cpp
)

target_link_libraries(
    ${PROJECT_NAME}
    PUBLIC
    Eigen3::Eigen
    Boost::date_time
    Boost::filesystem
    Boost::program_options
    Boost::system
    Boost::regex
    Boost::timer
    Boost::chrono
)

target_include_directories(
    ${PROJECT_NAME}
    PUBLIC
    ${OPENSMOKE_INCLUDE}
    ${CMAKE_CURRENT_LIST_DIR}/source
)

target_compile_options(${PROJECT_NAME}
    PRIVATE
    -Wno-unused-value
    -Wno-mismatched-new-delete
    -Wno-switch
)

# --------------------------------------------------------------------
# Installing options
# --------------------------------------------------------------------

install(TARGETS
    ${PROJECT_NAME}
    DESTINATION
    ${CMAKE_INSTALL_PREFIX}
)
