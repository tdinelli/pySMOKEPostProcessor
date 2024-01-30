#pragma once

// clang-format off
#include <OpenSMOKEpp>
#include <maps/Maps_CHEMKIN>
// clang-format on

class ProfilesDatabase {
 public:
  ProfilesDatabase(void);
  ~ProfilesDatabase(void);

  bool ReadKineticMechanism(const std::string &folder_name);

  bool ReadFileResults(const std::string &folder_name);

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

  std::vector<std::vector<double>> omega;
  std::vector<std::vector<double>> additional;

  unsigned int index_T;
  unsigned int index_P;
  unsigned int index_MW;
  unsigned int index_density;
  unsigned int index_velocity;
  unsigned int index_mass_flow_rate;
  unsigned int index_volume;

  unsigned int index_x_coord;
  unsigned int index_z_coord;

  std::vector<double> mw_species_;

  boost::property_tree::ptree xml_main_input;

  OpenSMOKE::ThermodynamicsMap_CHEMKIN *thermodynamicsMapXML;
  OpenSMOKE::KineticsMap_CHEMKIN *kineticsMapXML;

  bool iSensitivityEnabled_;
  bool iROPAEnabled_;
  bool is_kinetics_available_;

  boost::filesystem::path path_folder_results_;
  boost::filesystem::path path_folder_mechanism_;

  void ReactionsAssociatedToSpecies(const unsigned int index,
                                    std::vector<unsigned int> &indices);

  void isReactantProduct(const unsigned int reaction_index, double &netStoichiometry);

  std::string name_reactions_;
  std::vector<std::string> reaction_strings_;
};
