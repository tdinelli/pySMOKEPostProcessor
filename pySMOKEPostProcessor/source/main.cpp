/*-----------------------------------------------------------------------*\
|    ___                   ____  __  __  ___  _  _______                  |
|   / _ \ _ __   ___ _ __ / ___||  \/  |/ _ \| |/ / ____| _     _         |
|  | | | | '_ \ / _ \ '_ \\___ \| |\/| | | | | ' /|  _| _| |_ _| |_       |
|  | |_| | |_) |  __/ | | |___) | |  | | |_| | . \| |__|_   _|_   _|      |
|   \___/| .__/ \___|_| |_|____/|_|  |_|\___/|_|\_\_____||_|   |_|        |
|        |_|                                                              |
|                                                                         |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>				  |
|			 Edoardo Ramalli <edoardo.ramalli@polimi.it>				  |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano                                                 |
|   P.zza Leonardo da Vinci 32, 20133 Milano                              |
|                                                                         |
|-------------------------------------------------------------------------|
|                                                                         |
|   This file is part of OpenSMOKE++ framework.                           |
|                                                                         |
|	License																  |
|                                                                         |
|   Copyright(C) 2016-2012  Alberto Cuoci                                 |
|   OpenSMOKE++ is free software: you can redistribute it and/or modify   |
|   it under the terms of the GNU General Public License as published by  |
|   the Free Software Foundation, either version 3 of the License, or     |
|   (at your option) any later version.                                   |
|                                                                         |
|   OpenSMOKE++ is distributed in the hope that it will be useful,        |
|   but WITHOUT ANY WARRANTY; without even the implied warranty of        |
|   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         |
|   GNU General Public License for more details.                          |
|                                                                         |
|   You should have received a copy of the GNU General Public License     |
|   along with OpenSMOKE++. If not, see <http://www.gnu.org/licenses/>.   |
|                                                                         |
\*-----------------------------------------------------------------------*/

// Standard library
#include <sstream>
#include <vector>

// OpenSMOKEpp library
#include "OpenSMOKEpp"
#include "maps/Maps_CHEMKIN"
#include "maps/FluxAnalysisMap.h"
#include "newFluxMap.h"
#include "math/PhysicalConstants.h"
#include "kernel/kinetics/KineticsUtilityFunctions.h"

// Boost library
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

#include "PostProcessor.h"

bool VERBOSE = false;
/*
// Windows extern "C" __declspec(dllexport)
#ifdef _WIN32 || _WIN64
extern "C" __declspec(dllexport)
#else
extern "C"
#endif
int pyROPAPostProcessor(
    char* kineticFolder,
    char* outputFolder,
    char* specie,
    int command,
    int ropa_type,
	int ordering_type,
	int normalization_type,
    double ropa_local_value,
    double ropa_region_lower_value,
    double ropa_region_upper_value,
    double* coefficients,
    int* reactions,
    int len)
{

	std::string postprocessorType = "ropa";

	if (command == 0)
	{
		postprocessorType = "ropa";
	}
	else
	{
		return -1;
	}
	
	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	PostProcessor.Prepare(specie, ropa_type, ropa_local_value, 
					ropa_region_lower_value, ropa_region_upper_value,
					normalization_type, ordering_type);


	return PostProcessor.ComputeROPAPython(coefficients, reactions, len);

	return 0;
}

#ifdef _WIN32 || _WIN64
extern "C" __declspec(dllexport)
#else
extern "C"
#endif
int pySensitivityPostProcessor(
	char* kineticFolder,
	char* outputFolder,
	char* specie,
	int command,
	int sensitivity_type,
	int ordering_type,
	int normalization_type,
	double sensitivity_local_value,
	double sensitivity_region_lower_value,
	double sensitivity_region_upper_value,
	double* coefficients,
	int* reactions,
	int len) 
{
	std::string postprocessorType = "sensitivity";
	if (command == 0) 
	{
		postprocessorType = "sensitivity";
	}
	else 
	{
		return -1;
	}

	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	PostProcessor.Prepare(specie, sensitivity_type, sensitivity_local_value, 
				sensitivity_region_lower_value, sensitivity_region_upper_value, 
				normalization_type, ordering_type);

	return PostProcessor.ComputeSensitivityPython(coefficients, reactions, len);

	return 0;
}

#ifdef _WIN32 || _WIN64
extern "C" __declspec(dllexport)
#else
extern "C"
#endif
int FluxAnalysis(char* kineticFolder,
	char* outputFolder,
	char* specie,
	char* element,
	int command,
	int type, // 1-production 0-destruction
	double ropa_local_value,
	int thickness, // 0-absolute 1-relative(%)
	bool thicknesslogscale,
	int labeltype, // 0-absolute 1-relative(%)
	int depth,
	int width,
	double threshold)
{
	std::string postprocessorType = "fluxanalysis";

	PostProcessor* pp;
    pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);
	pp->PrepareFlux(specie, element, type, ropa_local_value, thickness, 
					thicknesslogscale, labeltype, depth, width, threshold);

}*/
int main() 
{
	
	PostProcessor PostProcessor("ropa", "/home/tdinelli/Desktop/ROPA/kinetics", "/home/tdinelli/Desktop/ROPA/Output");
	
	PostProcessor.PrepareFlux("H2","H",0,0.003258,0,true,1,2,5,0.010);
	PostProcessor.ComputeFluxPython();
	return 0;
}
