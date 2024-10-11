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

void merge_positive_and_negative_bars(const std::vector<size_t> &positive_indices,
                                      const std::vector<size_t> &negative_indices,
                                      const std::vector<double> &positive_coefficients,
                                      const std::vector<double> &negative_coefficients,
                                      std::vector<int> &indices,
                                      std::vector<double> &coefficients) {
  size_t n = positive_indices.size() + negative_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  for (size_t i = 0; i < positive_coefficients.size(); i++) {
    indices[i] = positive_indices[i];
    coefficients[i] = positive_coefficients[i];
    signum[i] = 1;
  }
  for (size_t i = 0; i < negative_coefficients.size(); i++) {
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

  for (size_t i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }
}

void MergeBars(const std::vector<size_t> &total_indices,
               const std::vector<double> &total_coefficients, std::vector<int> &indices,
               std::vector<double> &coefficients) {
  size_t n = total_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  for (size_t i = 0; i < total_indices.size(); i++) {
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

  for (size_t i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }
}

void MergeBars(const std::vector<size_t> &total_indices,
               const std::vector<double> &total_coefficients,
               const std::vector<double> &total_peaks, std::vector<int> &indices,
               std::vector<double> &coefficients, std::vector<double> &peaks) {
  size_t n = total_indices.size();

  std::vector<int> signum(n);

  indices.resize(n);
  coefficients.resize(n);
  peaks.resize(n);
  for (size_t i = 0; i < total_indices.size(); i++) {
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

  for (size_t i = 0; i < n; i++) {
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
  }

  OpenSMOKE_Utilities::ReorderPairsOfVectors(tmp1, peaks);
  std::reverse(peaks.begin(), peaks.end());
}
