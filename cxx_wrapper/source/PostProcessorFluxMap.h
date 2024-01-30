#pragma once

// clang-format off
#include <OpenSMOKEpp>
#include <maps/Maps_CHEMKIN>
#include <maps/FluxAnalysisMap.h>
// clang-format on

namespace pySMOKEPostProcessor {
class PostProcessorFluxMap : public OpenSMOKE::FluxAnalysisMap {
 public:
  PostProcessorFluxMap(OpenSMOKE::ThermodynamicsMap_CHEMKIN &thermodynamicsMapXML,
                       OpenSMOKE::KineticsMap_CHEMKIN &kineticsMapXML);

  void ComputeFluxAnalysis();
  void ComputeValues(const unsigned int index_j, std::vector<unsigned int> &local_indices,
                     std::vector<double> &local_thickness,
                     std::vector<double> &local_normal_fluxes,
                     std::vector<double> &local_fluxes);

  std::vector<int> IndexFirstName;
  std::vector<int> IndexSecondName;
  std::vector<double> ComputedLabelValue;
  std::vector<double> ComputedThicknessValue;
};
}  // namespace pySMOKEPostProcessor
