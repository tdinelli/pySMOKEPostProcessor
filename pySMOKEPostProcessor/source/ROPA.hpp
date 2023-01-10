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

#include "math/OpenSMOKEUtilities.h"
#include <algorithm>

ROPA::ROPA(const std::string kineticFolder, 
			std::string outputFolder, 
			std::string ropaType, 
			std::string species, 
			double localValue, 
			double lowerBound, 
			double upperBound)
{
	ropaType_ = ropaType;
	kineticFolder_ = kineticFolder;
	outputFolder_ = outputFolder;
	species_ = species;

	localValue_ = localValue;
	upperBound_ = upperBound;
	lowerBound_ = lowerBound;

}

void ROPA::SetDatabase(ProfilesDatabase* data)
{
	data_ = data;
}

void ROPA::ROPA_Calculations()
{
	// Select y variables among the species
	if (std::find(data_->string_list_massfractions_sorted.begin(), data_->string_list_massfractions_sorted.end(), species_) != data_->string_list_massfractions_sorted.end())
	{
		speciesIsSelected = true;
	}
	else 
	{
		std::cout << " ERROR: Please select an existing specie." << std::endl;
		exit(-1);
	}
	
	unsigned int index_of_species;
	for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++)
		if (speciesIsSelected == true)
			if (species_ == data_->string_list_massfractions_sorted[j])
			{
				index_of_species = data_->sorted_index[j];

				// debug check 
				//std::cout << "index: " << j << std::endl;
				//std::cout << "species: " << species_ << std::endl;
				//std::cout << "founded: " << data_->string_list_massfractions_sorted[j] << std::endl;
				
				break;
			}

	{
		OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
		OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
		OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());

		// Local Analysis
		if (ropaType_ == "local")
		{
			unsigned int index = 0;
			for (unsigned int j = 0; j < data_->number_of_abscissas_; j++)
				if (data_->additional[0][j] >= localValue_)
				{
					index = j;
					break;
				}

			// Recovers mass fractions
			for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
				omega[k + 1] = data_->omega[k][index];

			// Calculates mole fractions
			double MWmix;
			data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix, omega.GetHandle());

			// Calculates concentrations
			const double P_Pa = data_->additional[data_->index_P][index];
			const double T = data_->additional[data_->index_T][index];
			const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
			Product(cTot, x, &c);

			// Calculates formations rates
			data_->kineticsMapXML->SetTemperature(T);
			data_->kineticsMapXML->SetPressure(P_Pa);
			data_->thermodynamicsMapXML->SetTemperature(T);
			data_->thermodynamicsMapXML->SetPressure(P_Pa);

			data_->kineticsMapXML->KineticConstants();
			data_->kineticsMapXML->ReactionRates(c.GetHandle());

			// Ropa
			OpenSMOKE::ROPA_Data ropa;
			data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

			std::vector<int> reaction_indices;
			std::vector<double> reaction_coefficients;
			// qua devo agire ioooooo
			MergePositiveAndNegativeBars(ropa.production_reaction_indices[index_of_species],
				ropa.destruction_reaction_indices[index_of_species],
				ropa.production_coefficients[index_of_species], ropa.destruction_coefficients[index_of_species],
				reaction_indices, reaction_coefficients);

			// The OpenSMOKE ROPA Analysis returns 0-based indices that needs to be
			// transformed into 1-based indices before calling the Widget_Horizontal_Bars
			for (unsigned int i = 0; i < reaction_indices.size(); i++)
				reaction_indices[i]++;

			std::vector<std::string> production_reaction_names(reaction_indices.size());
			for (unsigned int i = 0; i < reaction_indices.size(); i++)
				production_reaction_names[i] = data_->reaction_strings_[reaction_indices[i] - 1];

			// PRINTAGGIO RISULTATI
			
			std::cout << "\ncoefficients \t\t indices \t\t names\n" << std::endl;
			for (int i = 0; i < reaction_coefficients.size(); i++)
			{
				std::cout << reaction_coefficients[i] << "\t\t" << reaction_indices[i] << "\t\t" << production_reaction_names[i] << std::endl;
			}
		} // Global | Region
		else
		{
			unsigned int index_min = 0;
			unsigned int index_max = data_->number_of_abscissas_ - 1;
			if (ropaType_ == "region")
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

			std::vector<double> global_production_coefficients;
			std::vector<double> global_destruction_coefficients;
			std::vector<unsigned int> global_production_reaction_indices;
			std::vector<unsigned int> global_destruction_reaction_indices;

			for (unsigned int j = index_min; j < index_max - 1; j++)
			{
				// Recovers mass fractions
				for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
					omega[k + 1] = data_->omega[k][j];

				// Calculates mole fractions
				double MWmix;
				data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix, omega.GetHandle());

				// Calculates concentrations
				const double P_Pa = data_->additional[data_->index_P][j];
				const double T = data_->additional[data_->index_T][j];
				const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
				Product(cTot, x, &c);

				// Calculates formations rates
				data_->kineticsMapXML->SetTemperature(T);
				data_->kineticsMapXML->SetPressure(P_Pa);
				data_->thermodynamicsMapXML->SetTemperature(T);
				data_->thermodynamicsMapXML->SetPressure(P_Pa);

				data_->kineticsMapXML->KineticConstants();
				data_->kineticsMapXML->ReactionRates(c.GetHandle());

				// Ropa
				OpenSMOKE::ROPA_Data ropa;
				data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

				if (ropa.production_coefficients[index_of_species].size() != ropa.production_reaction_indices[index_of_species].size() ||
					ropa.destruction_coefficients[index_of_species].size() != ropa.destruction_reaction_indices[index_of_species].size())
				{
					std::cout << "SSS" << std::endl;
				}

				if (j == index_min)
				{
					global_production_coefficients.resize(ropa.production_coefficients[index_of_species].size());
					global_destruction_coefficients.resize(ropa.destruction_coefficients[index_of_species].size());
					global_production_reaction_indices = ropa.production_reaction_indices[index_of_species];
					global_destruction_reaction_indices = ropa.destruction_reaction_indices[index_of_species];

				}

				const double dt = (data_->additional[0][j + 1] - data_->additional[0][j]) / delta;
				for (unsigned int k = 0; k < ropa.production_coefficients[index_of_species].size(); k++)
					global_production_coefficients[k] += dt * ropa.production_coefficients[index_of_species][k];

				for (unsigned int k = 0; k < ropa.destruction_coefficients[index_of_species].size(); k++)
					global_destruction_coefficients[k] += dt * ropa.destruction_coefficients[index_of_species][k];
			}

			std::vector<int> reaction_indices;
			std::vector<double> reaction_coefficients;
			// same shit di sopra qua devo agire io
			MergePositiveAndNegativeBars(global_production_reaction_indices,
				global_destruction_reaction_indices,
				global_production_coefficients, global_destruction_coefficients,
				reaction_indices, reaction_coefficients);

			// The OpenSMOKE ROPA Analysis returns 0-based indices that needs to be
			// transformed into 1-based indices before calling the Widget_Horizontal_Bars
			for (unsigned int i = 0; i < reaction_indices.size(); i++)
				reaction_indices[i]++;

			std::vector<std::string> production_reaction_names(reaction_indices.size());
			for (unsigned int i = 0; i < reaction_indices.size(); i++)
				production_reaction_names[i] = data_->reaction_strings_[reaction_indices[i] - 1];

			// PRINTAGGIO RISULTATI

			std::cout << "\ncoefficients \t\t indices \t\t names\n" << std::endl;
			for (int i = 0; i < reaction_coefficients.size(); i++)
			{
				std::cout << reaction_coefficients[i] << "\t\t" << reaction_indices[i] << "\t\t" << production_reaction_names[i] << std::endl;
			}
		}

	}

}

int ROPA::ROPA_Calculations_Python(double* coefficients, int* reactions, int len)
{
	// Select y variables among the species
	if (std::find(data_->string_list_massfractions_sorted.begin(), data_->string_list_massfractions_sorted.end(), species_) != data_->string_list_massfractions_sorted.end())
	{
		speciesIsSelected = true;
	}
	else
	{
		return -5;
	}
	unsigned int index_of_species;
	for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++){
		if (speciesIsSelected == true)
			if (species_ == data_->string_list_massfractions_sorted[j])
			{
				index_of_species = data_->sorted_index[j];
				break;
			}
	}

    OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());

    std::vector<int> reaction_indices;
    std::vector<double> reaction_coefficients;

    // Local Analysis
    if (ropaType_ == "local")
    {
        unsigned int index = 0;
        for (unsigned int j = 0; j < data_->number_of_abscissas_; j++)
            if (data_->additional[0][j] >= localValue_)
            {
                index = j;
                break;
            }

        // Recovers mass fractions
        for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
            omega[k + 1] = data_->omega[k][index];

        // Calculates mole fractions
        double MWmix;
        data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix, omega.GetHandle());

        // Calculates concentrations
        const double P_Pa = data_->additional[data_->index_P][index];
        const double T = data_->additional[data_->index_T][index];
        const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
        Product(cTot, x, &c);

        // Calculates formations rates
        data_->kineticsMapXML->SetTemperature(T);
        data_->kineticsMapXML->SetPressure(P_Pa);
        data_->thermodynamicsMapXML->SetTemperature(T);
        data_->thermodynamicsMapXML->SetPressure(P_Pa);

        data_->kineticsMapXML->KineticConstants();
        data_->kineticsMapXML->ReactionRates(c.GetHandle());

        // Ropa
        OpenSMOKE::ROPA_Data ropa;
        data_->kineticsMapXML->RateOfProductionAnalysis(ropa);


        // qua devo agire ioooooo
        MergePositiveAndNegativeBars(ropa.production_reaction_indices[index_of_species],
            ropa.destruction_reaction_indices[index_of_species],
            ropa.production_coefficients[index_of_species], ropa.destruction_coefficients[index_of_species],
            reaction_indices, reaction_coefficients);

        // The OpenSMOKE ROPA Analysis returns 0-based indices that needs to be
        // transformed into 1-based indices before calling the Widget_Horizontal_Bars
//        for (unsigned int i = 0; i < reaction_indices.size(); i++)
//            reaction_indices[i]++;
//
//        std::vector<std::string> production_reaction_names(reaction_indices.size());
//        for (unsigned int i = 0; i < reaction_indices.size(); i++)
//            production_reaction_names[i] = data_->reaction_strings_[reaction_indices[i] - 1];

        // PRINTAGGIO RISULTATI


    } // Global | Region
    else
    {
        unsigned int index_min = 0;
        unsigned int index_max = data_->number_of_abscissas_ - 1;
        if (ropaType_ == "region")
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

        std::vector<double> global_production_coefficients;
        std::vector<double> global_destruction_coefficients;
        std::vector<unsigned int> global_production_reaction_indices;
        std::vector<unsigned int> global_destruction_reaction_indices;

        for (unsigned int j = index_min; j < index_max - 1; j++)
        {
            // Recovers mass fractions
            for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
                omega[k + 1] = data_->omega[k][j];

            // Calculates mole fractions
            double MWmix;
            data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix, omega.GetHandle());

            // Calculates concentrations
            const double P_Pa = data_->additional[data_->index_P][j];
            const double T = data_->additional[data_->index_T][j];
            const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
            Product(cTot, x, &c);

            // Calculates formations rates
            data_->kineticsMapXML->SetTemperature(T);
            data_->kineticsMapXML->SetPressure(P_Pa);
            data_->thermodynamicsMapXML->SetTemperature(T);
            data_->thermodynamicsMapXML->SetPressure(P_Pa);

            data_->kineticsMapXML->KineticConstants();
            data_->kineticsMapXML->ReactionRates(c.GetHandle());

            // Ropa
            OpenSMOKE::ROPA_Data ropa;
            data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

            if (ropa.production_coefficients[index_of_species].size() != ropa.production_reaction_indices[index_of_species].size() ||
                ropa.destruction_coefficients[index_of_species].size() != ropa.destruction_reaction_indices[index_of_species].size())
            {
                std::cout << "SSS" << std::endl;
            }

            if (j == index_min)
            {
                global_production_coefficients.resize(ropa.production_coefficients[index_of_species].size());
                global_destruction_coefficients.resize(ropa.destruction_coefficients[index_of_species].size());
                global_production_reaction_indices = ropa.production_reaction_indices[index_of_species];
                global_destruction_reaction_indices = ropa.destruction_reaction_indices[index_of_species];

            }

            const double dt = (data_->additional[0][j + 1] - data_->additional[0][j]) / delta;
            for (unsigned int k = 0; k < ropa.production_coefficients[index_of_species].size(); k++)
                global_production_coefficients[k] += dt * ropa.production_coefficients[index_of_species][k];

            for (unsigned int k = 0; k < ropa.destruction_coefficients[index_of_species].size(); k++)
                global_destruction_coefficients[k] += dt * ropa.destruction_coefficients[index_of_species][k];
        }

        // same shit di sopra qua devo agire io
        MergePositiveAndNegativeBars(global_production_reaction_indices,
            global_destruction_reaction_indices,
            global_production_coefficients, global_destruction_coefficients,
            reaction_indices, reaction_coefficients);

        // The OpenSMOKE ROPA Analysis returns 0-based indices that needs to be
        // transformed into 1-based indices before calling the Widget_Horizontal_Bars
		//        for (unsigned int i = 0; i < reaction_indices.size(); i++)
		//            reaction_indices[i]++;
		//
			//        std::vector<std::string> production_reaction_names(reaction_indices.size());
		//        for (unsigned int i = 0; i < reaction_indices.size(); i++)
		//            production_reaction_names[i] = data_->reaction_strings_[reaction_indices[i] - 1];

    }

    for (int i = 0; i < std::min<int>(len, reaction_coefficients.size()); i++){
        coefficients[i] = reaction_coefficients[i];
        reactions[i] = reaction_indices[i];
    }

    return 0;

}

int ROPA::FluxAnalysis(std::string element, std::string thickness,
					std::string type, std::string labeltype, 
					int depth, int width, double threshold, 
					bool thicknesslogscale, int* indexFirstName, 
					int* indexSecondName, double* computedThickness, 
					double* computedLabel, int* lenght)
{
	// Select y variables among the species
	if (std::find(data_->string_list_massfractions_sorted.begin(), data_->string_list_massfractions_sorted.end(), species_) != data_->string_list_massfractions_sorted.end())
	{
		speciesIsSelected = true;
	}
	else
	{
		std::cout << "The selcted specie is not present inside the kinetic mechanism." << std::endl;
		exit(-1);
	}
	unsigned int index_of_species;
	for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++){
		if (speciesIsSelected == true)
		{
			if (species_ == data_->string_list_massfractions_sorted[j])
			{
				index_of_species = data_->sorted_index[j];
				break;
			}
		}
	}

	unsigned int index_element; // = ui.comboBox_Elements->currentIndex();
	std::vector<std::string> elements_names = data_->thermodynamicsMapXML->elements();
	for(unsigned int k = 0; k < elements_names.size(); k++)
	{
		if(element == elements_names[k])
		{
			index_element = k;	
			break;		
		}
	}
	const double n_elements = data_->thermodynamicsMapXML->atomic_composition()(index_of_species, index_element);

	if (n_elements == 0.)
	{
		std::cout << "The selected species does not contain the selected element" << std::endl;
		exit(-1);
	}

	const int max_depth = depth;
	const int max_width = width;
	const double min_threshold_percentage = threshold;

	// Local Analysis (Flux can be done only in when local ropa is available) 
    unsigned int index = 0;
    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++)
	{
        if (data_->additional[0][j] >= localValue_)
        {
            index = j;
            break;
        }
	}
	OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
	OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
	OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());
	OpenSMOKE::OpenSMOKEVectorDouble r(data_->kineticsMapXML->NumberOfReactions());

	// Recovers mass fractions
	for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
	{
		omega[k + 1] = data_->omega[k][index];
	}
	// Calculates mole fractions
	double MWmix;
	data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix, omega.GetHandle());

	// Calculates concentrations
	const double P_Pa = data_->additional[data_->index_P][index];
	const double T = data_->additional[data_->index_T][index];
	const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
	Product(cTot, x, &c);

	// Calculates formations rates
	data_->kineticsMapXML->SetTemperature(T);
	data_->kineticsMapXML->SetPressure(P_Pa);
	data_->thermodynamicsMapXML->SetTemperature(T);
	data_->thermodynamicsMapXML->SetPressure(P_Pa);

	data_->kineticsMapXML->KineticConstants();
	data_->kineticsMapXML->ReactionRates(c.GetHandle());
	data_->kineticsMapXML->GiveMeReactionRates(r.GetHandle());

	// OpenSMOKE::FluxAnalysisMap flux_analysis(*data_->thermodynamicsMapXML, *data_->kineticsMapXML);
	pySMOKEPostProcessor::PostProcessorFluxMap flux_analysis(*data_->thermodynamicsMapXML, *data_->kineticsMapXML);
	
	bool destruction = false;
	bool relativethickness = false;
	bool labelrelative = false;

	if(type == "destruction")
	{
		destruction = true;
	}
	if(thickness == "relative")
	{
		relativethickness = true;
	}
	if(labeltype == "relative")
	{
		labelrelative = true;
	}
	flux_analysis.SetDestructionAnalysis(destruction);
	flux_analysis.SetNormalThickness(relativethickness);
	flux_analysis.SetNormalTags(labelrelative);
	flux_analysis.SetLogarithmicThickness(thicknesslogscale);
	flux_analysis.SetMaxDepth(max_depth);
	flux_analysis.SetMaxWidth(max_width);
	flux_analysis.SetMinPercentageThreshold(min_threshold_percentage);
	flux_analysis.SetAtom(index_element);
	flux_analysis.SetReactionRates(r.Size(), r.GetHandle());

	std::vector<unsigned int> important_indices;
	important_indices.push_back(index_of_species);
	flux_analysis.GloballyAnalyze(important_indices, 0);
	flux_analysis.CalculateThickness();
	
	flux_analysis.ComputeFluxAnalysis();
	
	std::vector<int> firstName = flux_analysis.IndexFirstName;
	std::vector<int> secondName = flux_analysis.IndexSecondName;
	std::vector<double> thicknessValues = flux_analysis.ComputedThicknessValue;
	std::vector<double> labelValues = flux_analysis.ComputedLabelValue;

	for(int i = 0; i <= std::min<int>(firstName.size(), 1000); i++){
		indexFirstName[i] = firstName[i];
		indexSecondName[i] = secondName[i];
		computedThickness[i] = thicknessValues[i];
		computedLabel[i] = labelValues[i];
		lenght[i] = std::min<int>(firstName.size(), 1000);
	}

	return 0;
}

void ROPA::MergePositiveAndNegativeBars (const std::vector<unsigned int>& positive_indices,
	const std::vector<unsigned int>& negative_indices,
	const std::vector<double>& positive_coefficients,
	const std::vector<double>& negative_coefficients,
	std::vector<int>& indices,
	std::vector<double>& coefficients)
{
	unsigned int n = positive_indices.size() +
		negative_indices.size();

	std::vector<int> signum(n);

	indices.resize(n);
	coefficients.resize(n);
	for (unsigned int i = 0; i < positive_coefficients.size(); i++)
	{
		indices[i] = positive_indices[i];
		coefficients[i] = positive_coefficients[i];
		signum[i] = 1;
	}
	for (unsigned int i = 0; i < negative_coefficients.size(); i++)
	{
		indices[i + positive_indices.size()] = -negative_indices[i];
		coefficients[i + positive_indices.size()] = -negative_coefficients[i];
		signum[i + positive_indices.size()] = -1;
	}

	std::vector<double> tmp = coefficients;

	OpenSMOKE_Utilities::ReorderPairsOfVectors(coefficients, indices);
	std::reverse(indices.begin(), indices.end());
	std::reverse(coefficients.begin(), coefficients.end());

	OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp, signum);
	std::reverse(signum.begin(), signum.end());


	for (unsigned int i = 0; i < n; i++)
		if (signum[i] == -1)
		{
			indices[i] *= -1;
			coefficients[i] *= -1.;
		}

}
