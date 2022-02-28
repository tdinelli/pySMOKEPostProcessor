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
#ifndef UTILITIES_H
#define UTILITIES_H

#include <vector>
#include <string>

void MergePositiveAndNegativeBars
			(	const std::vector<unsigned int>& positive_indices, 
				const std::vector<unsigned int>& negative_indices,
				const std::vector<double>& positive_coefficients, 
				const std::vector<double>& negative_coefficients, 
				std::vector<int>& indices,
				std::vector<double>& coefficients);

void MergeBars( const std::vector<unsigned int>& total_indices, 
				const std::vector<double>& total_coefficients, 
				std::vector<int>& indices,
				std::vector<double>& coefficients);

void MergeBars( const std::vector<unsigned int>& total_indices, 
				const std::vector<double>& total_coefficients, 
				const std::vector<double>& total_peaks,
				std::vector<int>& indices,
				std::vector<double>& coefficients, 
				std::vector<double>& peaks);

#endif // UTILITIES_H

