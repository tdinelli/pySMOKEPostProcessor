// clang-format off
/*-----------------------------------------------------------------------*\
|                                                                         |
|                        _____  __  ___ ____   __ __  ______              |
|          ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____   |
|         / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \  |
|        / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /  |
|       / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/   |
|      /_/     /____/                                   /_/    /_/        |
|                                                                         |
|                                                                         |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>                  |
|            Edoardo Ramalli <edoardo.ramalli@polimi.it>				          |
|            Luna Pratali Maffei <luna.pratali@polimi.it>                 |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano       |
\*-----------------------------------------------------------------------*/
// clang-format on
#pragma once

class ProfilesDatabase {
 public:
  ProfilesDatabase();

  ~ProfilesDatabase();

  void read_kinetic_mechanism(const std::string &folder_name);

  void read_file_results(const std::string &folder_name);

  void species_coarsening(const double threshold);

  void reactions_associated_to_species(const size_t index, std::vector<size_t> &indices);

  void is_reactant_product(const size_t reaction_index, double &netStoichiometry);

  const static void py_wrap(pybind11::module_ &);

  std::unique_ptr<OpenSMOKE::ThermodynamicsMap_CHEMKIN> thermodynamics_map_xml_;

  std::unique_ptr<OpenSMOKE::KineticsMap_CHEMKIN> kinetics_map_xml_;

  const std::vector<std::string> &string_list_massfractions_sorted() const {
    return string_list_massfractions_sorted_;
  };

  const std::vector<size_t> &sorted_index() const { return sorted_index_; };

  const size_t &number_of_abscissas() const { return number_of_abscissas_; };

  const size_t &number_of_ordinates() const { return number_of_ordinates_; };

  const std::vector<std::vector<double>> &omega() const { return omega_; };

  const std::vector<std::vector<double>> &additional() const { return additional_; };

  const size_t &index_T() const { return index_T_; };

  const size_t &index_P() const { return index_P_; };

 private:
  void read_xml();

  bool is_sensitivity_enabled_;

  bool is_ropa_enabled_;

  bool is_kinetics_available_;

  size_t index_density_;

  size_t index_velocity_;

  size_t index_mass_flow_rate_;

  std::vector<std::vector<double>> omega_;
  std::vector<std::vector<double>> additional_;
  std::vector<std::string> reaction_strings_;

  boost::property_tree::ptree xml_main_input_;

  size_t index_T_;
  size_t index_P_;
  size_t index_MW_;
  size_t index_volume_;

  size_t index_x_coord_;
  size_t index_z_coord_;

  size_t number_of_abscissas_;
  size_t number_of_ordinates_;

  std::vector<size_t> index_of_massfractions_profiles_;
  std::vector<std::string> list_additional_;
  std::vector<size_t> conversion_species_;

  std::vector<std::string> string_list_massfractions_sorted_;
  std::vector<size_t> sorted_index_;
  std::vector<size_t> current_sorted_index;
  std::vector<double> sorted_max;

  std::vector<double> mw_species_;

  std::string name_reactions_;
};

#include "ProfilesDatabase.hpp"
