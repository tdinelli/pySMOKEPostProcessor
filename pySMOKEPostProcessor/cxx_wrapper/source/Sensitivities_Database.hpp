// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|                              _____  __  ___ ____   __ __  ______                   |
|                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        |
|               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       |
|              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       |
|             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        |
|            /_/     /____/                                   /_/    /_/             |
|                                                                                    |
|                                                                                    |
| ---------------------------------------------------------------------------------- |
| Please refer to the copyright statement and license                                |
| information at the end of this file.                                               |
| ---------------------------------------------------------------------------------- |
|                                                                                    |
|         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   |
|                  Luna Pratali Maffei <luna.pratali@polimi.it>                      |
|                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   |
|                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   |
|                                                                                    |
|         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 |
|         Department of Chemistry, Materials and Chemical Engineering                |
|         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on

Sensitivities_Database::Sensitivities_Database() {}

Sensitivities_Database::~Sensitivities_Database() {}

void Sensitivities_Database::SetDatabase(ProfilesDatabase *data) { data_ = data; }

void Sensitivities_Database::read_parent_file() {
  boost::filesystem::path path_results = data_->path_folder_results_ / "Sensitivities.xml";
  boost::property_tree::read_xml((path_results).string(), xml_main_input);

  std::stringstream stream;
  stream.str(xml_main_input.get<std::string>("opensmoke.variables"));

  stream >> number_of_variables_;

  names_.resize(number_of_variables_);
  local_index_.resize(number_of_variables_);
  global_index_.resize(number_of_variables_);
  for (size_t j = 0; j < number_of_variables_; j++) {
    stream >> names_[j];
    stream >> local_index_[j];
    stream >> global_index_[j];
  }

  std::stringstream stream;
  stream.str(xml_main_input.get<std::string>("opensmoke.n-parameters"));

  stream >> number_of_parameters_;
  parameters_.resize(number_of_parameters_);
  std::stringstream stream;
  stream.str(xml_main_input.get<std::string>("opensmoke.constant-parameters"));

  for (size_t j = 0; j < number_of_parameters_; j++) {
    stream >> parameters_[j];
  }

  std::stringstream stream;
  stream.str(xml_main_input.get<std::string>("opensmoke.points"));

  stream >> number_of_points_;

  // Memory allocation
  coefficients_.resize(number_of_parameters_);
  for (size_t j = 0; j < number_of_parameters_; j++) {
    coefficients_[j].resize(number_of_points_);
  }
  variable_.resize(number_of_points_);

  // Names of reactions
  string_list_reactions_.reserve(number_of_parameters_);
  for (size_t j = 0; j < number_of_parameters_; j++) {
    if (j + 1 <= data_->kineticsMapXML->NumberOfReactions()) {
      std::stringstream index;
      index << j + 1;
      std::string tmp = "R" + index.str() + ": " + data_->reaction_strings_[j];
      string_list_reactions_.push_back(tmp);
    } else {
      size_t local_index = j + 1 - data_->kineticsMapXML->NumberOfReactions();
      if (local_index <= data_->kineticsMapXML->NumberOfFallOffReactions()) {
        size_t global_index = data_->kineticsMapXML->IndicesOfFalloffReactions()[local_index - 1];
        std::stringstream index;
        index << global_index;
        std::string tmp = "R" + index.str() + "(inf): " + data_->reaction_strings_[global_index - 1];
        string_list_reactions_.push_back(tmp);
      } else {
        size_t global_index =
            data_->kineticsMapXML
                ->IndicesOfCabrReactions()[local_index - data_->kineticsMapXML->NumberOfReactions() - 1];
        std::stringstream index;
        index << global_index;
        std::string tmp = "R" + index.str() + "(inf): " + data_->reaction_strings_[global_index - 1];
        string_list_reactions_.push_back(tmp);
      }
    }
  }
}

void Sensitivities_Database::read_from_child_file(const std::string name) {
  std::string local_name = "Sensitivities." + name + ".xml";
  boost::property_tree::ptree ptree;
  try {
    boost::filesystem::path path_file = data_->path_folder_results_ / local_name;
    boost::property_tree::read_xml((path_file).string(), ptree);
  } catch (...) {
    throw std::runtime_error(" The file named: " + to_string(name) +
                             " it is not present in the output folder select another specie.");
  }

  boost::optional<boost::property_tree::ptree &> child = ptree.get_child_optional("opensmoke.coefficients");

  if (!child) {
    throw std::runtime_error("Corrupted xml file: missing the coefficients leaf");
  } else {
    std::stringstream stream;
    stream.str(ptree.get<std::string>("opensmoke.coefficients"));

    for (size_t i = 0; i < number_of_points_; i++) {
      for (size_t j = 0; j < number_of_parameters_; j++) {
        stream >> coefficients_[j][i];
      }
    }
  }

  for (size_t j = 0; j < number_of_variables_; j++) {
    if (names_[j] == name) {
      current_local_index_ = j;
      break;
    }
  }

  if (name == "temperature") {
    variable_ = data_->additional[data_->index_T];
  } else if (name == "density") {
    variable_ = data_->additional[data_->index_density];
  } else if (name == "velocity") {
    variable_ = data_->additional[data_->index_velocity];
  } else if (name == "mass-flow-rate") {
    variable_ = data_->additional[data_->index_mass_flow_rate];
  } else {
    // recognizing the global index of species
    size_t species_index;
    for (size_t j = 0; j < data_->string_list_massfractions_sorted.size(); j++) {
      if (name == data_->string_list_massfractions_sorted[j]) {
        species_index = data_->sorted_index[j];
        break;
      }
    }

    // from mass to mole fractions
    for (size_t i = 0; i < number_of_points_; i++) {
      variable_[i] =
          data_->omega[species_index][i] * data_->additional[data_->index_MW][i] / data_->mw_species_[species_index];
    }
  }
}

// zero-based
std::vector<double> Sensitivities_Database::normalized_profile(const size_t index, bool local_normalization) {
  std::vector<double> profile = coefficients_[index];
  if (local_normalization == true) {
    const double local_threshold = 1.e-16;

    for (size_t i = 0; i < number_of_points_; i++) {
      if (fabs(variable_[i]) > local_threshold) {
        profile[i] *= parameters_[index] / variable_[i];
      } else {
        profile[i] = 0.;
      }
    }
  } else {
    double normalization_coefficient = -1.e100;
    for (size_t i = 0; i < number_of_points_; i++) {
      if (fabs(variable_[i]) > normalization_coefficient) { normalization_coefficient = fabs(variable_[i]); }
    }
    const double normalization_coefficient_threshold = 1.e-100;
    if (normalization_coefficient > normalization_coefficient_threshold) {
      for (size_t i = 0; i < number_of_points_; i++) {
        profile[i] *= parameters_[index] / normalization_coefficient;
      }
    } else {
      for (size_t i = 0; i < number_of_points_; i++) {
        profile[i] = 0.;
      }
    }
  }

  return profile;
}

// zero-based
double Sensitivities_Database::normalized_profile(const size_t index, bool local_normalization, size_t point) {
  if (local_normalization == true) {
    const double local_threshold = 1.e-16;

    if (fabs(variable_[point]) > local_threshold) {
      return coefficients_[index][point] * parameters_[index] / variable_[point];
    } else {
      return 0.;
    }
  } else {
    double normalization_coefficient = -1e100;
    for (size_t i = 0; i < number_of_points_; i++) {
      if (fabs(variable_[i]) > normalization_coefficient) { normalization_coefficient = fabs(variable_[i]); }
    }

    const double normalization_coefficient_threshold = 1.e-100;
    if (normalization_coefficient > normalization_coefficient_threshold) {
      return coefficients_[index][point] * parameters_[index] / normalization_coefficient;
    } else {
      return 0.;
    }
  }
}

void Sensitivities_Database::reactions_reset() {
  // Fill the reaction indices
  current_coarse_index_.resize(number_of_parameters_);
  for (size_t j = 0; j < number_of_parameters_; j++) {
    current_coarse_index_[j] = j + 1;
  }
}

void Sensitivities_Database::reactions_coarsening(const double threshold) {
  // Fill the reaction indices
  std::vector<size_t> total_indices(number_of_parameters_);
  for (size_t j = 0; j < number_of_parameters_; j++) {
    total_indices[j] = j + 1;
  }

  // Evaluates the coefficients
  std::vector<double> total_coefficients(number_of_parameters_);
  std::vector<double> profile(data_->number_of_abscissas_);
  for (size_t j = 0; j < number_of_parameters_; j++) {
    profile = normalized_profile(j, false);

    double max_value = -1.e100;
    size_t max_index = 0;
    for (size_t i = 0; i < data_->number_of_abscissas_; i++)
      if (fabs(profile[i]) > max_value) {
        max_value = fabs(profile[i]);
        max_index = i;
      }
    total_coefficients[j] = profile[max_index];
  }

  // Reorder the coefficients
  std::vector<int> indices;
  std::vector<double> coefficients;
  MergeBars(total_indices, total_coefficients, indices, coefficients);

  current_coarse_index_.resize(0);
  if (fabs(coefficients[0]) > 0.) {
    for (size_t j = 0; j < number_of_parameters_; j++) {
      if (fabs(coefficients[j]) / fabs(coefficients[0]) > threshold) {
        current_coarse_index_.push_back(indices[j]);
      } else {
        break;
      }
    }
  }
}
// clang-format off
/*----------------------------------------------------------------------------------*\
|                                                                                    |
|         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            |
|         Copyright (C) 2024                                                         |
|             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        |
|             Luna Pratali Maffei <luna.pratali@polimi.it>                           |
|             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        |
|             Andrea Nobili       <anobili@stanford.edu>                             |
|                                                                                    |
|         This program is free software: you can redistribute it and/or modify       |
|         it under the terms of the GNU General Public License as published by       |
|         the Free Software Foundation, either version 3 of the License, or          |
|         (at your option) any later version.                                        |
|                                                                                    |
|         This program is distributed in the hope that it will be useful,            |
|         but WITHOUT ANY WARRANTY; without even the implied warranty of             |
|         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              |
|         GNU General Public License for more details.                               |
|                                                                                    |
|         You should have received a copy of the GNU General Public License          |
|         along with this program.  If not, see <https://www.gnu.org/licenses/>.     |
|                                                                                    |
\*----------------------------------------------------------------------------------*/
// clang-format on
