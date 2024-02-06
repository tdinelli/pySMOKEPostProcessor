#ifndef SENSITIVITIES_H
#define SENSITIVITIES_H

#include "ProfilesDatabase.h"
#include "Sensitivities_Database.h"

class Sensitivities {
 public:
  Sensitivities();

  ~Sensitivities();

  void SetDatabase(ProfilesDatabase* data);

  void SetNormalizationType(const std::string& normalizationType);

  void SetSensitivityType(const std::string& sensitivityType);

  void SetOrderingType(const std::string& orderingType);

  void SetTarget(const std::string& target);

  void SetLocalValue(const double& localValue);

  void SetLowerBound(const double& lowerBound);

  void SetUpperBound(const double& upperBound);

  void Prepare();

  void Sensitivity_Analysis(const unsigned int& number_of_reactions);

  void ReadSensitvityCoefficients();

  void GetSensitivityProfile(const unsigned int& reaction_index);

  const std::vector<unsigned int>& reactions() const { return reactions_; };

  const std::vector<double>& senitivityCoefficients() const {
    return sensitivity_coefficients_;
  };

 private:
  ProfilesDatabase* data_;

  Sensitivities_Database* sensitivities;

  std::string normalizationType_;
  std::string sensitivityType_;
  std::string orderingType_;
  std::string target_;

  double localValue_;
  double lowerBound_;
  double upperBound_;

  bool iLocalNormalization = false;
  std::vector<double> sensitivity_coefficients_;
  std::vector<unsigned int> reactions_;
};

#include "Sensitivities.hpp"
#endif  // SENSITIVITIES_H
