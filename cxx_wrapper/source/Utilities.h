#ifndef UTILITIES_H
#define UTILITIES_H

void MergePositiveAndNegativeBars(const std::vector<unsigned int> &positive_indices,
                                  const std::vector<unsigned int> &negative_indices,
                                  const std::vector<double> &positive_coefficients,
                                  const std::vector<double> &negative_coefficients,
                                  std::vector<int> &indices,
                                  std::vector<double> &coefficients);

void MergeBars(const std::vector<unsigned int> &total_indices,
               const std::vector<double> &total_coefficients, std::vector<int> &indices,
               std::vector<double> &coefficients);

void MergeBars(const std::vector<unsigned int> &total_indices,
               const std::vector<double> &total_coefficients,
               const std::vector<double> &total_peaks, std::vector<int> &indices,
               std::vector<double> &coefficients, std::vector<double> &peaks);

#include "Utilities.hpp"
#endif  // UTILITIES_H
