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

#include "ProfilesDatabase.h"

typedef std::variant<double, size_t, std::string, bool> multi_type;

class ROPA {
 public:
  ROPA(const std::unordered_map<std::string, multi_type>& ropa_settings);

  void set_database(ProfilesDatabase* data);

  void rate_of_production_analysis(const size_t number_of_reactions);

  // void RateOfProductionAnalysis2D(const size_t number_of_reactions, const double
  // local_x,
  //                                 const double local_z, const double region_low_x,
  //                                 const double region_up_x, const double region_low_z,
  //                                 const double region_up_z);

  void flux_analysis();

  void get_reaction_rates(const std::vector<size_t>& reaction_indices,
                          const bool sum_rates);

  void get_formation_rates(const std::string species, const std::string units,
                           const std::string type);

  const std::vector<size_t>& reactions() const { return reactions_; };

  const std::vector<double>& coefficients() const { return coefficients_; };

  const std::vector<size_t>& index_first_name() const { return index_first_name_; };

  const std::vector<size_t>& index_second_name() const { return index_second_name_; };

  const std::vector<double>& computed_thickness() const { return computed_thickness_; };

  const std::vector<double>& computed_labels() const { return computed_labels_; };

  const std::vector<double>& formation_rates() const { return formation_rates_; };

  const std::vector<std::vector<double>>& reaction_rates() const {
    return reaction_rates_;
  };

  const std::vector<double>& sum_of_rates() const { return sum_of_rates_; };

  const static void py_wrap(pybind11::module_&);

 private:
  // The inputs of this function are determined by opensmoke...
  void merge_positive_and_negative_bars(
      const std::vector<unsigned int>& positive_indices,
      const std::vector<unsigned int>& negative_indices,
      const std::vector<double>& positive_coefficients,
      const std::vector<double>& negative_coefficients, std::vector<int>& indices,
      std::vector<double>& coefficients);

  ProfilesDatabase* data_;
  std::vector<size_t> indices_coarse_reactions_;
  std::vector<std::string> string_list_reactions;

  std::string ropa_type_;
  std::string species_;

  double local_value_;
  double upper_bound_;
  double lower_bound_;
  bool species_is_selected_;

  std::string element_;
  std::string thickness_;
  std::string flux_analysis_type_;
  size_t width_;
  size_t depth_;
  double threshold_;
  bool thicknesslogscale_;
  std::string label_type_;

  std::vector<size_t> reactions_;
  std::vector<double> coefficients_;

  std::vector<size_t> index_first_name_;
  std::vector<size_t> index_second_name_;
  std::vector<double> computed_thickness_;
  std::vector<double> computed_labels_;

  std::vector<double> formation_rates_;
  std::vector<std::vector<double>> reaction_rates_;
  std::vector<double> sum_of_rates_;
};

#include "ROPA.hpp"
