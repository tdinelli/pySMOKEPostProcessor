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

#include "Sensitivities.h"

#include "ProfilesDatabase.h"
#include "Sensitivities_Database.h"
#include "Utilities.h"

Sensitivities::Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie)
{
	normalizationType_ = normalizationType;
	sensitivityType_ = sensitivityType;
	orderingType_ = orderingType;
	specie_ = specie;
}

Sensitivities::Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie, double localValue)
{
	normalizationType_ = normalizationType;
	sensitivityType_ = sensitivityType;
	orderingType_ = orderingType;
	localValue_ = localValue;
	specie_ = specie;
}

Sensitivities::Sensitivities(std::string normalizationType, std::string sensitivityType, std::string orderingType, std::string specie,double lowerBound, double upperBound)
{
	normalizationType_ = normalizationType;
	sensitivityType_ = sensitivityType;
	orderingType_ = orderingType;
	lowerBound_ = lowerBound;
	upperBound_ = upperBound;
	specie_ = specie;
}

Sensitivities::~Sensitivities()
{
}

void Sensitivities::SetDatabase(ProfilesDatabase* data)
{
	data_ = data;
}

void Sensitivities::Prepare()
{
	sensitivities = new Sensitivities_Database();
	sensitivities->SetDatabase(data_);
	sensitivities->ReadParentFile();

	// Widget: variables y
	// Non so se serve questa shit
	{
		std::vector<std::string> string_list_variables_y;
		string_list_variables_y.reserve(sensitivities->number_of_variables());
		for(unsigned int j=0;j<sensitivities->number_of_variables();j++)
			string_list_variables_y.push_back(sensitivities->names()[j]);
	}

}

void Sensitivities::Sensitivities_PostProcessing()
{
	bool iLocalNormalization;
	if (normalizationType_ == "local")
	{
		iLocalNormalization = true;
	}
	else if (normalizationType_ == "maxvalue") 
	{
		iLocalNormalization = false;
	}

	if (sensitivityType_ == "local")
	{
		// Find the point index
		unsigned int index = 0;
		for(unsigned int j=0;j<data_->number_of_abscissas_;j++)
			if (data_->additional[0][j] >= localValue_ )
			{
				index = j;
				break;
			}

		// Fill the reaction indices
			std::vector<unsigned int> total_indices(sensitivities->number_of_parameters());
		for (unsigned int j=0;j<sensitivities->number_of_parameters();j++)
			total_indices[j] = j+1;

		// Evaluates the coefficients
		std::vector<double> total_coefficients(sensitivities->number_of_parameters());
		for (unsigned int j=0;j<sensitivities->number_of_parameters();j++)
			total_coefficients[j] = sensitivities->NormalizedProfile(j, iLocalNormalization, index);

		// Reorder the coefficients
		std::vector<int> indices;
		std::vector<double> coefficients;
		MergeBars( total_indices, total_coefficients, indices, coefficients);

		// Fill the vector containing the reaction strings
		std::vector<std::string> reaction_names(indices.size());
		for(unsigned int i=0;i<indices.size();i++)
			reaction_names[i] = sensitivities->string_list_reactions()[indices[i]-1];

		// Printaggio risultati

		std::cout << "\ncoefficients \t\t indices \t\t names\n" << std::endl;
		for (int i = 0; i < 25; i++)  // coefficients.size()
		{
			std::cout << coefficients[i] << "\t\t" << indices[i] << "\t\t" << reaction_names[i] << std::endl;
		}
	}

	else
	{
		unsigned int index_min = 0;
		unsigned int index_max = data_->number_of_abscissas_ - 1;
		if (sensitivityType_ == "region")
		{
			for (unsigned int j = 0; j < data_->number_of_abscissas_; j++)
				if (data_->additional[0][j] >= lowerBound_)
				{
					index_min = j;
					break;
				}

			for (unsigned int j = index_min; j < data_->number_of_abscissas_; j++)
				if (data_->additional[0][j] >= upperBound_)
				{
					index_max = j;
					break;
				}

			if (index_min == index_max)
			{
				if (index_max == data_->number_of_abscissas_ - 1)
					index_min = index_max - 1;
				else
					index_max = index_min + 1;
			}
		}


		const double delta = data_->additional[0][index_max] - data_->additional[0][index_min];

		// Fill the reaction indices
		std::vector<unsigned int> total_indices(sensitivities->number_of_parameters());
		for (unsigned int j = 0; j < sensitivities->number_of_parameters(); j++)
			total_indices[j] = j + 1;

		// Evaluates the coefficients
		std::vector<double> total_coefficients(sensitivities->number_of_parameters());
		std::vector<double> total_peaks(sensitivities->number_of_parameters());
		std::vector<double> profile(data_->number_of_abscissas_);

		for (unsigned int j = 0; j < sensitivities->number_of_parameters(); j++)
		{
			profile = sensitivities->NormalizedProfile(j, iLocalNormalization);

			if (orderingType_ == "peakvalues")
			{
				double max_value = -1.e100;
				unsigned int max_index = 0;
				for (unsigned int i = index_min; i < index_max; i++)
					if (fabs(profile[i]) > max_value)
					{
						max_value = fabs(profile[i]);
						max_index = i;
					}
				total_coefficients[j] = profile[max_index];
				total_peaks[j] = data_->additional[0][max_index];
			}
			else if (orderingType_ == "area")
			{
				double sum = 0;
				for (unsigned int i = index_min; i < index_max - 1; i++)
					sum += profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
				total_coefficients[j] = sum / delta;
			}
			else if (orderingType_ == "absolutearea")
			{
				double sumPlus = 0;
				double sumMinus = 0;
				for (unsigned int i = index_min; i < index_max - 1; i++)
				{
					if (profile[i] < 0.)
						sumMinus -= profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
					else
						sumPlus += profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
				}

				if (sumPlus > sumMinus) total_coefficients[j] = (sumPlus + sumMinus) / delta;
				else                    total_coefficients[j] = -(sumPlus + sumMinus) / delta;
			}
		}

		// Reorder the coefficients
		std::vector<int> indices;
		std::vector<double> coefficients;
		std::vector<double> peaks;

		if (orderingType_ == "peakvalues")
			MergeBars(total_indices, total_coefficients, total_peaks, indices, coefficients, peaks);
		else
			MergeBars(total_indices, total_coefficients, indices, coefficients);

		// Fill the vector containing the reaction strings
		std::vector<std::string> reaction_names(indices.size());
		for (unsigned int i = 0; i < indices.size(); i++)
			reaction_names[i] = sensitivities->string_list_reactions()[indices[i] - 1];

		if (orderingType_ == "peakvalues")
		{
			//horizontal_bars->setRectangles(	coefficients, indices, peaks, reaction_names);
			std::cout << "\ncoefficients \t\t indices \t\t names\n" << std::endl;
			for (int i = 0; i < 25; i++)  // coefficients.size()
			{
				std::cout << coefficients[i] << "\t\t" << indices[i] << "\t\t" << reaction_names[i] << std::endl;
			}
		}
		else 
		{
			std::cout << "\ncoefficients \t\t indices \t\t names\n" << std::endl;
			for (int i = 0; i < 25; i++)  // coefficients.size()
			{
				std::cout << coefficients[i] << "\t\t" << indices[i] << "\t\t" << reaction_names[i] << std::endl;
			}
		}
	}
}

void Sensitivities::ReadSensitvityCoefficients()
{
	if (specie_.size() == 0)
		return;

	sensitivities->ReadFromChildFile(specie_);
}

