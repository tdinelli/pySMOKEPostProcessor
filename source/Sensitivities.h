/*-----------------------------------------------------------------------*\
|    ___                   ____  __  __  ___  _  _______                  |
|   / _ \ _ __   ___ _ __ / ___||  \/  |/ _ \| |/ / ____| _     _         |
|  | | | | '_ \ / _ \ '_ \\___ \| |\/| | | | | ' /|  _| _| |_ _| |_       |
|  | |_| | |_) |  __/ | | |___) | |  | | |_| | . \| |__|_   _|_   _|      |
|   \___/| .__/ \___|_| |_|____/|_|  |_|\___/|_|\_\_____||_|   |_|        |
|        |_|                                                              |
|                                                                         |
|   Author: Alberto Cuoci <alberto.cuoci@polimi.it>                       |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano                                                 |
|   P.zza Leonardo da Vinci 32, 20133 Milano                              |
|																		  |
|   This file has been modified from the original OpenSMOKE postprocessor |
|	to adapt it in python.                                                |
|																		  |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>                  |
|			 Edoardo Ramalli <edoardo.ramalli@polimi.it>                  |
\*-----------------------------------------------------------------------*/

#ifndef SENSITIVITIES_H
#define SENSITIVITIES_H

#include <iostream>
#include "ProfilesDatabase.h"
#include "Sensitivities_Database.h"


class Sensitivities
{
	

public:
	Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie);

	Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie, double localValue);

	Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie, double lowerBound, double upperBound);

	~Sensitivities();

	void SetDatabase(ProfilesDatabase* data);
	
	void Prepare();

	void Sensitivities_PostProcessing();

	void ReadSensitvityCoefficients();

private:
	ProfilesDatabase* data_;
	
	Sensitivities_Database* sensitivities;

	std::string normalizationType_;
	std::string sensitivityType_;
	std::string orderingType_;
	std::string specie_;

	double localValue_;
	double lowerBound_;
	double upperBound_;
};

#endif // SENSITIVITIES_H
