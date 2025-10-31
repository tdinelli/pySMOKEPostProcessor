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
#include "Sensitivities_Database.h"

class Sensitivities
{

  public:
    Sensitivities();

    ~Sensitivities();

    void SetDatabase(ProfilesDatabase *data);

    void SetNormalizationType(std::string normalizationType);

    void SetSensitivityType(std::string sensitivityType);

    void SetOrderingType(std::string orderingType);

    void SetTarget(std::string target);

    void SetLocalValue(double localValue);

    void SetLowerBound(double lowerBound);

    void SetUpperBound(double upperBound);

    void Prepare();

    void Sensitivity_Analysis(const unsigned int number_of_reactions);

    void ReadSensitvityCoefficients();

    void GetSensitivityProfile(unsigned int reaction_index);
    
    inline const std::vector<unsigned int>& reactions() const {return reactions_;};
    
    inline const std::vector<double>& senitivityCoefficients() const {return sensitivity_coefficients_;};

  private:
    ProfilesDatabase *data_;

    Sensitivities_Database *sensitivities;

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
