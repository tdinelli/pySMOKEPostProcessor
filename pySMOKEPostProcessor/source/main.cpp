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
#include "PostProcessorFluxMap.h"
#include "math/PhysicalConstants.h"
#include "kernel/kinetics/KineticsUtilityFunctions.h"

// Boost library
#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

#include "PostProcessor.h"

extern "C" int getBoundary(
	char* kineticFolder, 
	char* outputFolder,
	double* maximum_domain,
	double* minimum_domain,
	double* middle_domain)
{
	ProfilesDatabase* data_;
	data_ = new ProfilesDatabase();
	data_->ReadFileResults(outputFolder);
	data_->ReadKineticMechanism(kineticFolder);

	double maximum = data_->additional[0][data_->number_of_abscissas_ - 1];
	double minimum = data_->additional[0][0];
	double middle = 0.50*(data_->additional[0][0]+data_->additional[0][data_->number_of_abscissas_-1]);

	for (int i = 0; i < 1; i++)
	{
		maximum_domain[i] = maximum;
		minimum_domain[i] = minimum;
		middle_domain[i] = middle;
	}
	return 0;
}

// Windows extern "C" __declspec(dllexport)
extern "C" int pyROPAPostProcessor(
    char* kineticFolder,
    char* outputFolder,
    char* specie,
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
	
	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	pp->Prepare(specie, ropa_type, ropa_local_value, 
				ropa_region_lower_value, ropa_region_upper_value,
				normalization_type, ordering_type);


	pp->ComputeROPAPython(coefficients, reactions, len);

	return 0;
}

extern "C" int pySensitivityPostProcessor(
	char* kineticFolder,
	char* outputFolder,
	char* target,
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

	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	pp->Prepare(target, sensitivity_type, sensitivity_local_value, 
				sensitivity_region_lower_value, sensitivity_region_upper_value, 
				normalization_type, ordering_type);

	pp->ComputeSensitivityPython(coefficients, reactions, len);

	return 0;
}

extern "C" int FluxAnalysis(char* kineticFolder,
	char* outputFolder,
	char* specie,
	char* element,
	int type, // 1-production 0-destruction
	double ropa_local_value,
	int thickness, // 0-absolute 1-relative(%)
	bool thicknesslogscale,
	int labeltype, // 0-absolute 1-relative(%)
	int depth,
	int width,
	double threshold,
	int* indexFirstName,
	int* indexSecondName,
	double* computedThickness,
	double* computedLabel,
	int* lenght)
{
	std::string postprocessorType = "fluxanalysis";

	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);
	pp->PrepareFlux(specie, element, type, ropa_local_value, thickness, 
					thicknesslogscale, labeltype, depth, width, threshold);
	pp->ComputeFluxPython(indexFirstName, indexSecondName, computedThickness, computedLabel, lenght);
	
	return 0;
}

extern "C" int GetReactionRates ( 
	char* kineticFolder, 
	char* outputFolder,
	int reaction_index,
	double* reaction_rate) 
{
	std::string postprocessorType = "ropa";
	
	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	pp->GiveMeReactionRate(reaction_index, reaction_rate);

	return 0;
}

extern "C" int GetFormationRates (
	char* kineticFolder, 
	char* outputFolder,
	char* specie,
	char* units,
	char* type,
	double* formation_rate
) 
{
	std::string postprocessorType = "ropa";
	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);

	pp->GiveMeFormationRate(specie, units, type, formation_rate);

	return 0;
}

extern "C" int GetSensitivityCoefficient(
	char* kineticFolder,
	char* outputFolder,
	int reaction_index,
	char* target,
	char* normalization_type,
	double* coefficient
)
{
	std::string postprocessorType = "sensitivity";
	std::cout << "CIOA" << std::endl;
	PostProcessor* pp;
	pp = new PostProcessor(postprocessorType, kineticFolder, outputFolder);

	pp->GiveMeSensitivityCoefficient(normalization_type, target, coefficient, reaction_index);

	return 0;
}

int main() 
{
	return 0;
}
