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
#pragma once
#include "ProfilesDatabase.h"
#include "Utilities.h"

class Sensitivities_Database {
 public:
  explicit Sensitivities_Database();

  ~Sensitivities_Database();

  void set_database(ProfilesDatabase *data);

  void read_parent_file();

  void read_from_child_file(const std::string name);

  std::vector<double> normalized_profile(const size_t index, bool local_normalization);

  double normalized_profile(const size_t index, bool local_normalization, size_t point);

  void ReactionsCoarsening(const double threshold);

  void ReactionsReset();

  const std::vector<std::string> &names() const { return names_; }

  size_t number_of_variables() const { return number_of_variables_; }

  const std::vector<double> &variable() const { return variable_; }

  const std::vector<std::string> &string_list_reactions() const { return string_list_reactions_; }

  const std::vector<size_t> &current_coarse_index() const { return current_coarse_index_; }

  size_t number_of_parameters() const { return number_of_parameters_; }

 private:

  ProfilesDatabase *data_;

  boost::property_tree::ptree xml_main_input;

  size_t number_of_variables_;
  size_t number_of_parameters_;
  size_t number_of_points_;
  size_t number_of_species_;
  std::vector<size_t> local_index_;
  std::vector<size_t> global_index_;
  std::vector<std::string> names_;
  std::vector<std::vector<double>> coefficients_;
  std::vector<double> parameters_;

  std::vector<double> variable_;
  size_t current_local_index_;

  std::vector<std::string> string_list_reactions_;
  std::vector<size_t> current_coarse_index_;
};

#include "Sensitivities_Database.hpp"
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
