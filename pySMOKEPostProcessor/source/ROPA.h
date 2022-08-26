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

#ifndef ROPA_H
#define ROPA_H

#include "ProfilesDatabase.h"

class ROPA 
{
public:
	// Global
	ROPA(const std::string kineticFolder, std::string outputFolder, std::string ropaType, std::string species);

	// Local
	ROPA(const std::string kineticFolder, std::string outputFolder, std::string ropaType, std::string species, double localValue);
	
	// Region
	ROPA(const std::string kineticFolder, std::string outputFolder, std::string ropaType, std::string species, double lowerBound, double upperBound);

	//Python
    ROPA(const std::string kineticFolder, std::string outputFolder, std::string ropaType, std::string species, double localValue, double lowerBound, double upperBound);

	void SetDatabase(ProfilesDatabase* data);

	void ROPA_Calculations();

    int ROPA_CalculationsPython(double* coefficients, int* reactions, int len);

	void MergePositiveAndNegativeBars (const std::vector<unsigned int>& positive_indices,
		const std::vector<unsigned int>& negative_indices,
		const std::vector<double>& positive_coefficients,
		const std::vector<double>& negative_coefficients,
		std::vector<int>& indices,
		std::vector<double>& coefficients);
	
	int FluxAnalysis(std::string element, std::string thickness,
					std::string type, std::string labeltype, 
					int depth, int width, double threshold, 
					bool thicknesslogscale,int* indexFirstName, 
					int* indexSecondName, double* computedThickness, 
					double* computedLabel, int* lenght);

private:

	ProfilesDatabase* data_;
	std::vector<unsigned int> indices_coarse_reactions_;
	std::vector<std::string> string_list_reactions;

	std::string ropaType_;
	std::string kineticFolder_;
	std::string outputFolder_;
	std::string species_;
	double localValue_;
	double upperBound_;
	double lowerBound_;
	bool speciesIsSelected;
};

#include "ROPA.hpp"
#endif // ROPA_H
