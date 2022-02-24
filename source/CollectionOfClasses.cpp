// Standard library
#include <sstream>

// Eigen
#include <Eigen/Dense>

// OpenSMOKE++ Library
#include "math/PhysicalConstants.h"
#include "kernel/thermo/ThermoPolicy_CHEMKIN.h"
#include "kernel/kinetics/ReactionPolicy_CHEMKIN.h"
#include "maps/ThermodynamicsMap_CHEMKIN.h"
#include "maps/TransportPropertiesMap_CHEMKIN.h"
#include "maps/KineticsMap_CHEMKIN.h"
#include "kernel/kinetics/KineticsUtilityFunctions.h"
#include "maps/FluxAnalysisMap.h"
#include "Utilities.h"

// Classes that need to be compiled
#include "Utilities.hpp"
#include "ProfilesDatabase.hpp"
#include "Sensitivities_Database.hpp"
#include "ROPA.hpp"
#include "Sensitivities.hpp"