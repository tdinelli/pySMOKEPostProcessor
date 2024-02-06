set(CXX_INCLUDES
     ${CMAKE_CURRENT_LIST_DIR}/PostProcessorFluxMap.h
     ${CMAKE_CURRENT_LIST_DIR}/ProfilesDatabase.h
     ${CMAKE_CURRENT_LIST_DIR}/ROPA.h
     ${CMAKE_CURRENT_LIST_DIR}/Sensitivities.h
     ${CMAKE_CURRENT_LIST_DIR}/Sensitivities_Database.h
     ${CMAKE_CURRENT_LIST_DIR}/Utilities.h
)

set_property(GLOBAL PROPERTY CXX_INCLUDES_PROP "${CXX_INCLUDES}")
