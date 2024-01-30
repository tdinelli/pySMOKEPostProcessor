#ifndef SENSITIVITIES_DATABASE_H
#define SENSITIVITIES_DATABASE_H

#include "ProfilesDatabase.h"
#include "Utilities.h"

class Sensitivities_Database {
 public:
  Sensitivities_Database(void);
  ~Sensitivities_Database(void);

  void SetDatabase(ProfilesDatabase *data);

  void ReadParentFile();
  void ReadFromChildFile(const std::string name);
  std::vector<double> NormalizedProfile(const unsigned int index,
                                        bool local_normalization);
  double NormalizedProfile(const unsigned int index, bool local_normalization,
                           unsigned int point);

  boost::property_tree::ptree xml_main_input;

  const std::vector<std::string> &names() const { return names_; }
  unsigned int number_of_variables() const { return number_of_variables_; }
  const std::vector<double> &variable() const { return variable_; }

  const std::vector<std::string> &string_list_reactions() const {
    return string_list_reactions_;
  }
  const std::vector<unsigned int> &current_coarse_index() const {
    return current_coarse_index_;
  }

  void ReactionsCoarsening(const double threshold);
  void ReactionsReset();

  unsigned int number_of_parameters() const { return number_of_parameters_; }

 private:
  ProfilesDatabase *data_;
  unsigned int number_of_variables_;
  unsigned int number_of_parameters_;
  unsigned int number_of_points_;
  unsigned int number_of_species_;
  std::vector<unsigned int> local_index_;
  std::vector<unsigned int> global_index_;
  std::vector<std::string> names_;
  std::vector<std::vector<double>> coefficients_;
  std::vector<double> parameters_;

  std::vector<double> variable_;
  unsigned int current_local_index_;

  std::vector<std::string> string_list_reactions_;
  std::vector<unsigned int> current_coarse_index_;
};

#include "Sensitivities_Database.hpp"
#endif  // SENSITIVITIES_DATABASE_H
