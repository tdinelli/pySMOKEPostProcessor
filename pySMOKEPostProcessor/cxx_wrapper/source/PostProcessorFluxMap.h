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

namespace pySMOKEPostProcessor {
class PostProcessorFluxMap : public OpenSMOKE::FluxAnalysisMap {
 public:
  PostProcessorFluxMap(OpenSMOKE::ThermodynamicsMap_CHEMKIN &thermodynamicsMapXML,
                       OpenSMOKE::KineticsMap_CHEMKIN &kineticsMapXML);

  void ComputeFluxAnalysis();
  void ComputeValues(const size_t index_j, std::vector<unsigned int> &local_indices,
                     std::vector<double> &local_thickness,
                     std::vector<double> &local_normal_fluxes,
                     std::vector<double> &local_fluxes);

  std::vector<int> IndexFirstName;
  std::vector<int> IndexSecondName;
  std::vector<double> ComputedLabelValue;
  std::vector<double> ComputedThicknessValue;
};
}  // namespace pySMOKEPostProcessor

#include "PostProcessorFluxMap.hpp"
