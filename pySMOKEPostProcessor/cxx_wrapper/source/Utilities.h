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

void merge_positive_and_negative_bars(const std::vector<size_t> &positive_indices,
                                      const std::vector<size_t> &negative_indices,
                                      const std::vector<double> &positive_coefficients,
                                      const std::vector<double> &negative_coefficients,
                                      std::vector<int> &indices,
                                      std::vector<double> &coefficients);

void merge_bars(const std::vector<size_t> &total_indices,
                const std::vector<double> &total_coefficients, std::vector<int> &indices,
                std::vector<double> &coefficients);

void merge_bars(const std::vector<size_t> &total_indices,
                const std::vector<double> &total_coefficients,
                const std::vector<double> &total_peaks, std::vector<int> &indices,
                std::vector<double> &coefficients, std::vector<double> &peaks);

#include "Utilities.hpp"
