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

#include "ProfilesDatabase.h"

class PostProcessor
{
public:
	
	PostProcessor(std::string postprocessorType, std::string kineticFolder, std::string outputFolder);

	void Prepare(std::string specie, int type, double local_value, double lower_value, 
							double upper_value, int sensitivity_normalization_type, 
							int sensitivity_ordering_type);

	
	void PrepareFlux(std::string specie, std::string element, int type, double local_value,
					int thickness, bool thicknesslogscale, int labeltype, int depth, 
					int width, double threshold);

	int ComputeROPAPython(double* coefficients, int* reactions, int len);

	int ComputeSensitivityPython(double* coefficients, int* reactions, int len);

	int ComputeFluxPython(int* indexFirstName, int* indexSecondName, double* computedThickness, double* computedLabel, int* lenght);

	std::string Type_;
	std::string kineticFolder_;
	std::string outputFolder_;
	std::string species_;
	std::string element_;

	std::string normalizationType_;
	std::string orderingType_;

	double localValue_;
	double lowerBound_;
	double upperBound_;
	std::string thickness_;
	bool islogscale;
	std::string labeltype_;
	int depth_;
	int width_;
	double threshold_;

private:
	std::string postprocessorType_;
	ProfilesDatabase *data_;
};

#include "PostProcessor.hpp"
#endif // POSTPROCESSOR_H
