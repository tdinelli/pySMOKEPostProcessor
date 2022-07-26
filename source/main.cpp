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

#include <iostream>
#include "PostProcessor.h"

bool VERBOSE = false;

// Windows extern "C" __declspec(dllexport)
#ifdef _WIN32
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
    double ropa_local_value,
    double ropa_region_lower_value,
    double ropa_region_upper_value,
    double* coefficients,
    int* reactions,
    int len)
{

	std::string postprocessorType;

	if (command == 0)
	{
		postprocessorType = "ropa";
	}
	else
	{
		return -1;
	}
	
	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	int return_value = PostProcessor.PrepareROPAPython(specie, ropa_type, ropa_local_value, ropa_region_lower_value, ropa_region_upper_value);
	if (return_value != 0)
	{
	    return return_value;
	}
	return PostProcessor.ComputeROPAPython(coefficients, reactions, len);
	
	return 0;
}

#ifdef _WIN32
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
	std::string postprocessorType;
	if (command == 0) 
	{
		postprocessorType = "sensitivity";
	}
	else 
	{
		return -1;
	}

	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	int return_value = PostProcessor.PrepareSensitivityPython(specie, 
				sensitivity_type, 
				sensitivity_local_value, 
				sensitivity_region_lower_value, 
				sensitivity_region_upper_value, 
				normalization_type, 
				ordering_type);
	if (return_value != 0) {
		return return_value;
	}
	return PostProcessor.ComputeSensitivityPython(coefficients, reactions, len);

	return 0;
}

int main() 
{
	return 0;
}
