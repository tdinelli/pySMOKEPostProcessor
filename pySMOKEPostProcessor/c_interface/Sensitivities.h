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

#ifndef SENSITIVITIES_H
#define SENSITIVITIES_H

#include "ProfilesDatabase.h"
#include "Sensitivities_Database.h"

class Sensitivities
{
	

public:

	Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, 
					std::string specie, double localValue, double lowerBound, double upperBound);

	~Sensitivities();

	void SetDatabase(ProfilesDatabase* data);
	
	void Prepare();

	void Sensitivities_PostProcessing();

	int Sensitivities_Python_PostProcessing(double* sensitivity_coefficients, int* reactions, int len);

	int ReadSensitvityCoefficients();

	int GetSensitivityProfile(int reaction_index, double* coefficient);

private:
	ProfilesDatabase* data_;
	
	Sensitivities_Database* sensitivities;

	std::string normalizationType_;
	std::string sensitivityType_;
	std::string orderingType_;
	std::string target_;

	double localValue_;
	double lowerBound_;
	double upperBound_;
};

#include "Sensitivities.hpp"
#endif // SENSITIVITIES_H
