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

#ifndef ROPA_H
#define ROPA_H

#include <boost/filesystem.hpp>
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

    int ROPA_CalculationsPython(float* coefficients, int* reactions, int len);

	void MergePositiveAndNegativeBars (const std::vector<unsigned int>& positive_indices,
		const std::vector<unsigned int>& negative_indices,
		const std::vector<double>& positive_coefficients,
		const std::vector<double>& negative_coefficients,
		std::vector<int>& indices,
		std::vector<double>& coefficients);

private:

	ProfilesDatabase* data_;
	std::vector<unsigned int> indices_coarse_reactions_;
	std::vector<std::string> string_list_reactions;
	
	void FluxAnalysis();

	std::string ropaType_;
	std::string kineticFolder_;
	std::string outputFolder_;
	std::string species_;
	double localValue_;
	double upperBound_;
	double lowerBound_;
	bool speciesIsSelected;
};

#endif // ROPA_H
