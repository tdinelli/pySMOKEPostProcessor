#ifndef POSTPROCESSOR_DEFINITIONS_H
#define POSTPROCESSOR_DEFINITIONS_H

#ifndef POSTPROCESSOR_API
# ifdef _MSC_VER
#  define POSTPROCESSOR_API __declspec(dllexport)
# else
#  define POSTPROCESSOR_API
# endif
#endif // POSTPROCESSOR_API

// In the future think about removing this stuff from here
// include definition should be separated in each file

// Standard library
#include <sstream>
#include <vector>
#include <exception>
#include <stdexcept>
#include <string>
#include <iostream>
#include <numeric>

// OpenSMOKEpp library
#include "OpenSMOKE_Definitions.h"
#include "kernel/thermo/Thermodynamics_CHEMKIN"
#include "kernel/transport/Transport_CHEMKIN"
#include "kernel/kinetics/ReactionPolicy_CHEMKIN.h"
#include "maps/ThermodynamicsMap_CHEMKIN.h"
#include "maps/TransportPropertiesMap_CHEMKIN.h"
#include "maps/KineticsMap_CHEMKIN.h"
#include "maps/FluxAnalysisMap.h"
#include "math/PhysicalConstants.h"
#include "kernel/kinetics/KineticsUtilityFunctions.h"

// Boost library
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/program_options.hpp>

// Eigen 
#include <Eigen/Dense>

namespace PostProcessor
{
    class Exception : public std::exception
    {
        private:
            std::string __what;

        public:

        Exception(const std::string& what) : __what(what){}

        const char* what() const throw()
        {
            return this->__what.c_str();
        }
    };
} // namespace Post Processor

#endif // POSTPROCESSOR_DEFINITIONS_H