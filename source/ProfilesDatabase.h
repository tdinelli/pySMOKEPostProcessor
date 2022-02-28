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

#ifndef PROFILESDATABASE_H
#define PROFILESDATABASE_H

#include <iostream>

#include <boost/filesystem.hpp>
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/xml_parser.hpp>

namespace OpenSMOKE
{
	class ThermodynamicsMap_CHEMKIN;
	class KineticsMap_CHEMKIN;
}

class ProfilesDatabase
{
public:
	ProfilesDatabase(void);
	~ProfilesDatabase(void);

	bool ReadKineticMechanism(const std::string& folder_name);
	bool ReadFileResults(const std::string& folder_name);
	void Prepare();
	void SpeciesCoarsening(const double threshold);

	int number_of_abscissas_;
	int number_of_ordinates_;

	std::vector<int> column_index_of_massfractions_profiles;
	std::vector<std::string> string_list_additional;
	std::vector<int> list_of_conversion_species_;

	std::vector<std::string> string_list_massfractions_sorted;
	std::vector<int> sorted_index;
	std::vector<int> current_sorted_index;
	std::vector<double> sorted_max;

	std::vector< std::vector<double> > omega;
	std::vector< std::vector<double> > additional;

	unsigned int index_T;
	unsigned int index_P;
	unsigned int index_MW;
	unsigned int index_density;
	unsigned int index_velocity;
	unsigned int index_mass_flow_rate;

	std::vector<double> mw_species_;

	boost::property_tree::ptree xml_main_input;

	OpenSMOKE::ThermodynamicsMap_CHEMKIN* thermodynamicsMapXML;
	OpenSMOKE::KineticsMap_CHEMKIN* kineticsMapXML;

	bool iSensitivityEnabled_;
	bool iROPAEnabled_;
	bool is_kinetics_available_;

	boost::filesystem::path path_folder_results_;
	boost::filesystem::path path_folder_mechanism_;

	void ReactionsAssociatedToSpecies(const unsigned int index, std::vector<unsigned int>& indices);

	std::vector<std::string> reaction_strings_;
};

#endif // PROFILESDATABASE_H
