pybind11_add_module(${PROJECT_NAME}
    ${CMAKE_CURRENT_LIST_DIR}/PostProcessorWrapper_py.cpp
)

target_link_libraries(
    ${PROJECT_NAME}
    PRIVATE
        Eigen3::Eigen
)

# Link Boost libraries - modern Boost (1.70+) is mostly header-only
if(TARGET Boost::headers)
    # Modern Boost CONFIG mode (1.70+)
    target_link_libraries(${PROJECT_NAME} PRIVATE Boost::headers)
elseif(TARGET Boost::boost)
    # Alternative modern Boost target
    target_link_libraries(${PROJECT_NAME} PRIVATE Boost::boost)
else()
    # Legacy Boost with components (pre-1.70 or FindBoost module)
    target_link_libraries(
        ${PROJECT_NAME}
        PRIVATE
            Boost::date_time
            Boost::filesystem
            Boost::program_options
            Boost::system
            Boost::regex
            Boost::timer
            Boost::chrono
    )
endif()

target_include_directories(
    ${PROJECT_NAME}
    PRIVATE
        ${OPENSMOKE_INCLUDE}
        ${CMAKE_CURRENT_LIST_DIR}/source
)

# Compiler-specific warning suppression
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
  target_compile_options(${PROJECT_NAME}
        PRIVATE
            -Wno-unused-value
            -Wno-mismatched-new-delete
            -Wno-switch
    )
elseif(MSVC)
  target_compile_options(${PROJECT_NAME}
        PRIVATE
            /wd4018  # signed/unsigned mismatch
            /wd4267  # conversion warnings
    )
endif()

target_compile_definitions(${PROJECT_NAME}
    PRIVATE
        VERSION_INFO="${PROJECT_VERSION}"
)

# --------------------------------------------------------------------
# Installation
# --------------------------------------------------------------------
install(
    TARGETS ${PROJECT_NAME}
    LIBRARY DESTINATION .
    RUNTIME DESTINATION .
)
