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
#ifndef POSTPROCESSOR_H
#define POSTPROCESSOR_H

#include <boost/filesystem.hpp>

#include "ProfilesDatabase.h"

class PostProcessor
{
public:
	
	
	PostProcessor(std::string postprocessorType, std::string kineticFolder, std::string outputFolder);
	
	PostProcessor(std::string kineticFolder);

	void Prepare();

	int PrepareROPAPython(std::string specie, int ropa_type, double ropa_local_value, double ropa_region_lower_value, double ropa_region_upper_value);
	
	int PrepareSensitivityPython(std::string specie, int sensitivity_type, double sensitivity_local_value, double sensitivity_region_lower_value, double sensitivity_region_upper_value,
								int sensitivity_normalization_type, int sensitivity_ordering_type);

	void ComputeROPA();

	int ComputeROPAPython(double* coefficients, int* reactions, int len);

	int ComputeSensitivityPython(double* coefficients, int* reactions, int len);

	void SensitivityAnalysis();

	void PrintRecap_ROPA();

	void PrintRecap_SENSITIVITY();

	std::string ropaType_;
	std::string sensitivityType_;
	std::string kineticFolder_;
	std::string outputFolder_;
	std::string species_;

	std::string normalizationType_;
	std::string orderingType_;

	double localValue_;
	double lowerBound_;
	double upperBound_;
private:
	std::string postprocessorType_;
	ProfilesDatabase *data_;
};

#endif // POSTPROCESSOR_H
