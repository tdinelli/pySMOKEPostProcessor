// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|                              _____  __  ___ ____   __ __  ______                   |
|                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        |
|               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       |
|              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       |
|             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        |
|            /_/     /____/                                   /_/    /_/             |
|                                                                                    |
|                                                                                    |
| ---------------------------------------------------------------------------------- |
| Please refer to the copyright statement and license                                |
| information at the end of this file.                                               |
| ---------------------------------------------------------------------------------- |
|                                                                                    |
|         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   |
|                  Luna Pratali Maffei <luna.pratali@polimi.it>                      |
|                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   |
|                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   |
|                                                                                    |
|         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 |
|         Department of Chemistry, Materials and Chemical Engineering                |
|         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on

// Standard library
#include <sstream>
#include <vector>
#include <exception>
#include <stdexcept>
#include <string>
#include <iostream>
#include <numeric>

// OpenSMOKEpp library
#include <OpenSMOKE_Definitions.h>
#include <kernel/thermo/Thermodynamics_CHEMKIN>
#include <kernel/transport/Transport_CHEMKIN>
#include <kernel/kinetics/ReactionPolicy_CHEMKIN.h>
#include <kernel/kinetics/KineticsUtilityFunctions.h>
#include <maps/ThermodynamicsMap_CHEMKIN.h>
#include <maps/TransportPropertiesMap_CHEMKIN.h>
#include <maps/KineticsMap_CHEMKIN.h>
#include <maps/FluxAnalysisMap.h>
#include <math/PhysicalConstants.h>

// Boost library
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>
#include <boost/program_options.hpp>

// Eigen 
#include <Eigen/Dense>

// pyBIND11
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
namespace py = pybind11;
constexpr auto byref = py::return_value_policy::reference_internal;
constexpr auto call_guard = py::call_guard<py::gil_scoped_release>();

// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            |
|         Copyright (C) 2024                                                         |
|             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        |
|             Luna Pratali Maffei <luna.pratali@polimi.it>                           |
|             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        |
|             Andrea Nobili       <anobili@stanford.edu>                             |
|                                                                                    |
|         This program is free software: you can redistribute it and/or modify       |
|         it under the terms of the GNU General Public License as published by       |
|         the Free Software Foundation, either version 3 of the License, or          |
|         (at your option) any later version.                                        |
|                                                                                    |
|         This program is distributed in the hope that it will be useful,            |
|         but WITHOUT ANY WARRANTY; without even the implied warranty of             |
|         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              |
|         GNU General Public License for more details.                               |
|                                                                                    |
|         You should have received a copy of the GNU General Public License          |
|         along with this program.  If not, see <https://www.gnu.org/licenses/>.     |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on
