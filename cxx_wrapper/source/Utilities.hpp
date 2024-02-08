void MergePositiveAndNegativeBars(const std::vector<unsigned int> &positive_indices,
                                  const std::vector<unsigned int> &negative_indices,
                                  const std::vector<double> &positive_coefficients,
                                  const std::vector<double> &negative_coefficients,
                                  std::vector<int> &indices,
                                  std::vector<double> &coefficients) {
  unsigned int n = positive_indices.size() + negative_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  for (unsigned int i = 0; i < positive_coefficients.size(); i++) {
    indices[i] = positive_indices[i];
    coefficients[i] = positive_coefficients[i];
    signum[i] = 1;
  }
  for (unsigned int i = 0; i < negative_coefficients.size(); i++) {
    indices[i + positive_indices.size()] = -negative_indices[i];
    coefficients[i + positive_indices.size()] = -negative_coefficients[i];
    signum[i + positive_indices.size()] = -1;
  }

  std::vector<double> tmp = coefficients;

  OpenSMOKE_Utilities::ReorderPairsOfVectors(coefficients, indices);
  std::reverse(indices.begin(), indices.end());
  std::reverse(coefficients.begin(), coefficients.end());

  OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp, signum);
  std::reverse(signum.begin(), signum.end());

  for (unsigned int i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }
}

void MergeBars(const std::vector<unsigned int> &total_indices,
               const std::vector<double> &total_coefficients, std::vector<int> &indices,
               std::vector<double> &coefficients) {
  unsigned int n = total_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  for (unsigned int i = 0; i < total_indices.size(); i++) {
    if (total_coefficients[i] < 0.) {
      coefficients[i] = -total_coefficients[i];
      indices[i] = -total_indices[i];
      signum[i] = -1;
    } else {
      coefficients[i] = total_coefficients[i];
      indices[i] = total_indices[i];
      signum[i] = 1;
    }
  }

  std::vector<double> tmp = coefficients;

  OpenSMOKE_Utilities::ReorderPairsOfVectors(coefficients, indices);
  std::reverse(indices.begin(), indices.end());
  std::reverse(coefficients.begin(), coefficients.end());

  OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp, signum);
  std::reverse(signum.begin(), signum.end());

  for (unsigned int i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }
}

void MergeBars(const std::vector<unsigned int> &total_indices,
               const std::vector<double> &total_coefficients,
               const std::vector<double> &total_peaks, std::vector<int> &indices,
               std::vector<double> &coefficients, std::vector<double> &peaks) {
  unsigned int n = total_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  peaks.resize(n);
  for (unsigned int i = 0; i < total_indices.size(); i++) {
    if (total_coefficients[i] < 0.) {
      coefficients[i] = -total_coefficients[i];
      indices[i] = -total_indices[i];
      peaks[i] = total_peaks[i];
      signum[i] = -1;
    } else {
      coefficients[i] = total_coefficients[i];
      indices[i] = total_indices[i];
      peaks[i] = total_peaks[i];
      signum[i] = 1;
    }
  }

  std::vector<double> tmp = coefficients;
  std::vector<double> tmp1 = coefficients;

  OpenSMOKE_Utilities::ReorderPairsOfVectors(coefficients, indices);
  std::reverse(indices.begin(), indices.end());
  std::reverse(coefficients.begin(), coefficients.end());

  OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp, signum);
  std::reverse(signum.begin(), signum.end());

  for (unsigned int i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }

  OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp1, peaks);
  std::reverse(peaks.begin(), peaks.end());
}
