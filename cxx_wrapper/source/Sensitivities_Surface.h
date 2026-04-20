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
|   CRECK Modeling Group <www.creckmodeling.polimi.it>                    |
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

#ifndef SENSITIVITIES_SURFACE_H
#define SENSITIVITIES_SURFACE_H

#include "ProfilesDatabase.h"
#include "Sensitivities_Database_Surface.h"
#include "Sensitivities.h"

class Sensitivities_Surface: public virtual Sensitivities {
  public:
    Sensitivities_Surface();

    //~Sensitivities_Surface();

    void Prepare(bool heterogeneousSensitivity);

    void ReadSensitivityCoefficients();

    // To me, the Sensitivity_Analysis function should be exactly the same as the homogeneous case, as the difference is only in the file names 
    // (which is why Sensitvities_Database_Surface exists). However, I can't make this thing compile with call to standard parent function.
    void Sensitivity_Analysis(const unsigned int number_of_reactions);
    
  private:
    Sensitivities_Database_Surface* sensitivities_het;  
    // This thing is a mess, the issue is with the type of the pointer that changes with respect to parent.
    // this variable is the only reason why we need to duplicate the code of Sensitivity_Analysis.
    // In previous implementation where everything was duplicated, this variable was just called sensitivities as the homogeneous case
    // Now I changed the name for clarity

    bool heterogeneousSensitivity_;
};

#include "Sensitivities_Surface.hpp"
#endif  // SENSITIVITIES_H
