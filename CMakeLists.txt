#--------------------------------------------------------------------
# Preliminary Settings
#--------------------------------------------------------------------

cmake_minimum_required (VERSION 3.16)

project (pySMOKEpostprocessor)

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

if( NOT CMAKE_BUILD_TYPE)
  set (CMAKE_BUILD_TYPE Release)
endif()

message (STATUS "Compiling in mode: ${CMAKE_BUILD_TYPE}")

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

#set ( CPP_SOURCE_FILES 
#  pySMOKEPostProcessor/c_interface/source/Utilities.cpp
#  pySMOKEPostProcessor/c_interface/source/ProfilesDatabase.cpp
#)

#set (CPP_INCLUDE
#  pySMOKEPostProcessor/c_interface/source/Utilities.h
#  pySMOKEPostProcessor/c_interface/source/ProfilesDatabase.h
#)

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

add_library(pySMOKEPostProcessor SHARED
            ${C_INTERFACE_INCLUDE_FILES}
            ${C_INTERFACE_SOURCE_FILES}
)

#--------------------------------------------------------------------
# Installing options
#--------------------------------------------------------------------

install ( TARGETS pySMOKEPostProcessor 
          DESTINATION ${INSTALL_BIN_DIR}/bin)

#--------------------------------------------------------------------
# Packing options
#--------------------------------------------------------------------

set(CPACK_PACKAGE_NAME "pySMOKEPostProcessor")
set(CPACK_PACKAGE_VERSION_MAJOR ${PROJECT_VERSION_MAJOR})
set(CPACK_PACKAGE_VERSION_MINOR ${PROJECT_VERSION_MINOR})
set(CPACK_PACKAGE_VERSION_PATCH ${PROJECT_VERSION_PATCH})
set(CPACK_PACKAGE_VENDOR "CRECK modeling group")
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Python binder of the OpenSMOKEPostProcessor")

# Include whithin the package the compiled library
set(CPACK_COMPONENTS_ALL bin)
set(CPACK_COMPONENT_SOURCE_GROUP "Compiled Librayr")
set(CPACK_COMPONENT_SOURCE_DESCRIPTION "Compiled interface of pySMOKEPostProcessor")
set(CPACK_COMPONENTS_IGNORE_GROUPS ".*")
install ( TARGETS pySMOKEPostProcessor DESTINATION bin)

# Include whithin the package also the source code 
# both c_interface and python
set(CPACK_COMPONENTS_ALL source)
set(CPACK_COMPONENT_SOURCE_GROUP "Source code")
set(CPACK_COMPONENT_SOURCE_DESCRIPTION "Source code for c_interface and python of the pySMOKEPostProcessor")
set(CPACK_COMPONENTS_IGNORE_GROUPS ".*")
install ( DIRECTORY
            ${CMAKE_SOURCE_DIR}/c_interface
            ${CMAKE_SOURCE_DIR}/pySMOKEPostProcessor
          DESTINATION source
          PATTERN "*.pyc" EXCLUDE
          PATTERN "__pycache__*" EXCLUDE
        )

# Include boost libraries inside the packaging
set(CPACK_COMPONENTS_ALL lib)
set(CPACK_COMPONENT_SOURCE_GROUP "Boost libraries")
set(CPACK_COMPONENT_SOURCE_DESCRIPTION "Shared boost libraries")
set(CPACK_COMPONENTS_IGNORE_GROUPS ".*")
install ( TARGETS
            ${Boost_DATETIME_LIBRARY}
            ${Boost_FILE_SYSTEM_LIBRARY} 
            ${Boost_PROGRAMOPTIONS_LIBRARY}
            ${Boost_regex_LIBRARY}
            ${Boost_timer_LIBRARY}
            ${Boost_chrono_LIBRARY}
          DESTINATION lib
        )

# Imposta i dettagli del pacchetto
set(CPACK_GENERATOR "TGZ")
set(CPACK_SOURCE_GENERATOR "TGZ")
set(CPACK_SOURCE_IGNORE_FILES "/build/;/.git/;.gitignore;.vscode/")

set (CPACK)

include(CPack)