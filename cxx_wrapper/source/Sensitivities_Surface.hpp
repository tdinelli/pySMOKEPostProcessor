/*-----------------------------------------------------------------------*\
|    ___                   ____  __  __  ___  _  _______                  |
|   / _ \ _ __   ___ _ __ / ___||  \/  |/ _ \| |/ / ____| _     _         |
|  | | | | '_ \ / _ \ '_ \\___ \| |\/| | | | | ' /|  _| _| |_ _| |_       |
|  | |_| | |_) |  __/ | | |___) | |  | | |_| | . \| |__|_   _|_   _|      |
|   \___/| .__/ \___|_| |_|____/|_|  |_|\___/|_|\_\_____||_|   |_|        |
|        |_|                                                              |
|                                                                         |
|   Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>                  |
|            Edoardo Ramalli <edoardo.ramalli@polimi.it>                  |
|   CRECK Modeling Group <http://creckmodeling.chem.polimi.it>            |
|   Department of Chemistry, Materials and Chemical Engineering           |
|   Politecnico di Milano                                                 |
|   P.zza Leonardo da Vinci 32, 20133 Milano                              |
|                                                                         |
|-------------------------------------------------------------------------|
|                                                                         |
|   This file is part of OpenSMOKE++ framework.                           |
|                                                                         |
| License                                                                 |
|                                                                         |
|   Copyright(C) 2016-2012  Alberto Cuoci                                 |
|   OpenSMOKE++ is free software: you can redistribute it and/or modify   |
|   it under the terms of the GNU General Public License as published by  |
|   the Free Software Foundation, either version 3 of the License, or     |
|   (at your option) any later version.                                   |
|                                                                         |
|   OpenSMOKE++ is distributed in the hope that it will be useful,        |
|   but WITHOUT ANY WARRANTY; without even the implied warranty of        |
|   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         |
|   GNU General Public License for more details.                          |
|                                                                         |
|   You should have received a copy of the GNU General Public License     |
|   along with OpenSMOKE++. If not, see <http://www.gnu.org/licenses/>.   |
|                                                                         |
\*-----------------------------------------------------------------------*/

#include "ProfilesDatabase.h"
#include "Sensitivities_Database_Surface.h"
#include "Utilities.h"

Sensitivities_Surface::Sensitivities_Surface() {
  Sensitivities();
}

//Sensitivities_Surface::~Sensitivities_Surface() {}

void Sensitivities_Surface::Prepare(bool heterogeneousSensitivity) {
  heterogeneousSensitivity_ = heterogeneousSensitivity;
  sensitivities_het = new Sensitivities_Database_Surface();
  sensitivities_het->SetDatabase(data_);
  sensitivities_het->ReadParentFile(heterogeneousSensitivity_);

  // Widget: reactions
  {
    sensitivities_het->ReactionsReset();
  }
  // Widget: variables y
  {
    std::vector<std::string> string_list_variables_y;
    string_list_variables_y.reserve(sensitivities_het->number_of_variables());
    for (unsigned int j = 0; j < sensitivities_het->number_of_variables(); j++)
      string_list_variables_y.push_back(sensitivities_het->names()[j]);
  }
}

void Sensitivities_Surface::Sensitivity_Analysis(const unsigned int number_of_reactions) {
  std::vector<int> indices;
  std::vector<double> coefficients;

  if (sensitivityType_ == "local") {
    // Find the point index
    unsigned int index = 0;
    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[0][j] >= localValue_) {
        index = j;
        break;
      }
    }

    // Fill the reaction indices
    std::vector<unsigned int> total_indices(sensitivities_het->number_of_parameters());
    for (unsigned int j = 0; j < sensitivities_het->number_of_parameters(); j++)
      total_indices[j] = j + 1;

    // Evaluates the coefficients
    std::vector<double> total_coefficients(sensitivities_het->number_of_parameters());
    for (unsigned int j = 0; j < sensitivities_het->number_of_parameters(); j++)
      total_coefficients[j] = sensitivities_het->NormalizedProfile(j, iLocalNormalization, index);
    // Reorder the coefficients
    MergeBars(total_indices, total_coefficients, indices, coefficients);

    // Fill the vector containing the reaction strings
    std::vector<std::string> reaction_names(indices.size());
    for (unsigned int i = 0; i < indices.size(); i++)
      reaction_names[i] = sensitivities_het->string_list_reactions()[indices[i] - 1];
    

    // Printaggio risultati
    // for (int i = 0; i < std::min<int>(len, coefficients.size()); i++) {
    //	sensitivity_coefficients[i] = 2;// coefficients[i];
    //	reactions[i] = indices[i];
    //}//
  } else {
    unsigned int index_min = 0;
    unsigned int index_max = data_->number_of_abscissas_ - 1;
    if (sensitivityType_ == "region") {
      for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
        if (data_->additional[0][j] >= lowerBound_) {
          index_min = j;
          break;
        }
      }

      for (unsigned int j = index_min; j < data_->number_of_abscissas_; j++) {
        if (data_->additional[0][j] >= upperBound_) {
          index_max = j;
          break;
        }
      }

      if (index_min == index_max) {
        if (index_max == data_->number_of_abscissas_ - 1) {
          index_min = index_max - 1;
        } else {
          index_max = index_min + 1;
        }
      }
    }

    const double delta = data_->additional[0][index_max] - data_->additional[0][index_min];

    // Fill the reaction indices
    std::vector<unsigned int> total_indices(sensitivities_het->number_of_parameters());
    for (unsigned int j = 0; j < sensitivities_het->number_of_parameters(); j++)
      total_indices[j] = j + 1;

    // Evaluates the coefficients
    std::vector<double> total_coefficients(sensitivities_het->number_of_parameters());
    std::vector<double> total_peaks(sensitivities_het->number_of_parameters());
    std::vector<double> profile(data_->number_of_abscissas_);

    for (unsigned int j = 0; j < sensitivities_het->number_of_parameters(); j++) {
      profile = sensitivities_het->NormalizedProfile(j, iLocalNormalization);

      if (orderingType_ == "peak-values") {
        double max_value = -1.e100;
        unsigned int max_index = 0;
        for (unsigned int i = index_min; i < index_max; i++) {
          if (fabs(profile[i]) > max_value) {
            max_value = fabs(profile[i]);
            max_index = i;
          }
        }
        total_coefficients[j] = profile[max_index];
        total_peaks[j] = data_->additional[0][max_index];
      } else if (orderingType_ == "area") {
        double sum = 0;
        for (unsigned int i = index_min; i < index_max - 1; i++)
          sum += profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
        total_coefficients[j] = sum / delta;
      } else if (orderingType_ == "absolute-area") {
        double sumPlus = 0;
        double sumMinus = 0;
        for (unsigned int i = index_min; i < index_max - 1; i++) {
          if (profile[i] < 0.)
            sumMinus -= profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
          else
            sumPlus += profile[i] * (data_->additional[0][i + 1] - data_->additional[0][i]);
        }

        if (sumPlus > sumMinus)
          total_coefficients[j] = (sumPlus + sumMinus) / delta;
        else
          total_coefficients[j] = -(sumPlus + sumMinus) / delta;
      } else {
        throw std::invalid_argument(
            "Available ordering types are: peak-values | area | absolute-area");
      }
    }

    // Reorder the coefficients
    std::vector<double> peaks;

    if (orderingType_ == "peak-values")
      MergeBars(total_indices, total_coefficients, total_peaks, indices, coefficients, peaks);
    else
      MergeBars(total_indices, total_coefficients, indices, coefficients);

    // Fill the vector containing the reaction strings
    std::vector<std::string> reaction_names(indices.size());
    for (unsigned int i = 0; i < indices.size(); i++)
      reaction_names[i] = sensitivities_het->string_list_reactions()[indices[i] - 1];
  }
  // indices it's 1-based since we have to postprocess here it is returned 0-based
  sensitivity_coefficients_.resize(std::min<int>(number_of_reactions, coefficients.size()));
  reactions_.resize(std::min<int>(number_of_reactions, coefficients.size()));
  for (int i = 0; i < std::min<int>(number_of_reactions, coefficients.size()); i++) {
    sensitivity_coefficients_[i] = coefficients[i];
    reactions_[i] = indices[i] - 1;
  }
}

void Sensitivities_Surface::ReadSensitivityCoefficients() {
  if (target_ == "") throw std::invalid_argument("Select a target!");

  sensitivities_het->ReadFromChildFile(target_,heterogeneousSensitivity_);
}
