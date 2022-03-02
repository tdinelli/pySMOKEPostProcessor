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

#ifndef POSTPROCESSOR_H
#define POSTPROCESSOR_H

#include <boost/filesystem.hpp>

#include "ProfilesDatabase.h"

class PostProcessor
{
public:
	
	
	PostProcessor(std::string postprocessorType, std::string kineticFolder, std::string outputFolder);

	void Prepare();

	int PreparePython(std::string, int ropa_type, float ropa_local_value, float ropa_region_lower_value, float ropa_region_upper_value);

	void ComputeROPA();

	int ComputeROPAPython(float* coefficients, int* reactions, int len);

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
