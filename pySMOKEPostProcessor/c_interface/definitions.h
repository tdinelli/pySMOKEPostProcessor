#ifndef POSTPROCESSOR_DEFINITIONS_H
#define POSTPROCESSOR_DEFINITIONS_H

#ifndef POSTPROCESSOR_API
# ifdef _MSC_VER
#  define POSTPROCESSOR_API __declspec(dllexport)
# else
#  define POSTPROCESSOR_API
# endif
#endif // POSTPROCESSOR_API

// Standard library
#include <sstream>
#include <vector>

// OpenSMOKEpp library
#include <OpenSMOKEpp>
#include <maps/Maps_CHEMKIN>
#include <maps/FluxAnalysisMap.h>
#include <math/PhysicalConstants.h>
#include <kernel/kinetics/KineticsUtilityFunctions.h>

// Boost library
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

// #include <PostProcessorFluxMap.h>

#endif // POSTPROCESSOR_DEFINITIONS_H