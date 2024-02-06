#ifndef ROPA_H
#define ROPA_H

// clang-format off
#include "ProfilesDatabase.h"
#include "PostProcessorFluxMap.h"
// clang-format on

class ROPA {
 public:
  ROPA();

  void SetDatabase(ProfilesDatabase* data) { data_ = data; };

  void RateOfProductionAnalysis(const unsigned int& number_of_reactions);

  void RateOfProductionAnalysis2D(const unsigned int& number_of_reactions,
                                  const double& local_x, const double& local_z,
                                  const double& region_low_x, const double& region_up_x,
                                  const double& region_low_z, const double& region_up_z);

  void MergePositiveAndNegativeBars(const std::vector<unsigned int>& positive_indices,
                                    const std::vector<unsigned int>& negative_indices,
                                    const std::vector<double>& positive_coefficients,
                                    const std::vector<double>& negative_coefficients,
                                    std::vector<int>& indices,
                                    std::vector<double>& coefficients);

  void FluxAnalysis();

  void GetReactionRates(const std::vector<unsigned int>& reaction_indices,
                        const bool& sum_rates);

  void GetFormationRates(const std::string& specie, const std::string& units,
                         const std::string& type);

  void SetKineticFolder(const std::string& kineticFolder) {
    kineticFolder_ = kineticFolder;
  };

  void SetOutputFolder(const std::string& outputFolder) { outputFolder_ = outputFolder; };

  void SetROPAType(const std::string& kineticFolder);

  void SetSpecies(const std::string& species) { species_ = species; };

  void SetLocalValue(const double& localValue) { localValue_ = localValue; };

  void SetLowerBound(const double& lowerBound) { lowerBound_ = lowerBound; };

  void SetUpperBound(const double& upperBound) { upperBound_ = upperBound; };

  void SetElement(const std::string& element) { element_ = element; };

  void SetThickness(const std::string& thickness);

  void SetFluxAnalysisType(const std::string& type);

  void SetWidth(const int& width) { width_ = width; };

  void SetDepth(const int& depth) { depth_ = depth; };

  void SetThreshold(const double& threshold) { threshold_ = threshold; };

  void SetThicknessLogScale(const bool& thicknesslogscale) {
    thicknesslogscale_ = thicknesslogscale;
  };

  void SetLabelType(const std::string& type);

  const std::vector<unsigned int>& reactions() const { return reactions_; };

  const std::vector<double>& coefficients() const { return coefficients_; };

  const std::vector<int>& indexFirstName() const { return indexFirstName_; };

  const std::vector<int>& indexSecondName() const { return indexSecondName_; };

  const std::vector<double>& computedThickness() const { return computedThickness_; };

  const std::vector<double>& computedLabel() const { return computedLabel_; };

  const std::vector<double>& formationRates() const { return formationRates_; };

  const std::vector<std::vector<double>>& reactionRates() const {
    return reactionRates_;
  };

  const std::vector<double>& sumOfRates() const { return sumOfRates_; };

 private:
  ProfilesDatabase* data_;
  std::vector<unsigned int> indices_coarse_reactions_;
  std::vector<std::string> string_list_reactions;

  std::string ropaType_;
  std::string kineticFolder_;
  std::string outputFolder_;
  std::string species_;

  double localValue_;
  double upperBound_;
  double lowerBound_;
  bool speciesIsSelected;

  std::string element_;
  std::string thickness_;
  std::string flux_type_;
  int width_;
  int depth_;
  double threshold_;
  bool thicknesslogscale_;
  std::string label_type_;

  std::vector<unsigned int> reactions_;
  std::vector<double> coefficients_;

  std::vector<int> indexFirstName_;
  std::vector<int> indexSecondName_;
  std::vector<double> computedThickness_;
  std::vector<double> computedLabel_;

  std::vector<double> formationRates_;
  std::vector<std::vector<double>> reactionRates_;
  std::vector<double> sumOfRates_;
};

#include "ROPA.hpp"
#endif  // ROPA_H
