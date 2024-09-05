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

namespace pySMOKEPostProcessor {
PostProcessorFluxMap::PostProcessorFluxMap(
    OpenSMOKE::ThermodynamicsMap_CHEMKIN &thermodynamicsMapXML,
    OpenSMOKE::KineticsMap_CHEMKIN &kineticsMapXML)
    : OpenSMOKE::FluxAnalysisMap(thermodynamicsMapXML, kineticsMapXML) {}

void PostProcessorFluxMap::ComputeFluxAnalysis() {
  for (size_t j = 0; j < list_of_analyzed_species_.size(); j++) {
    const unsigned int index_j = list_of_analyzed_species_[j];
    ComputeValues(index_j, global_important_indices_[index_j], global_relative_thickness_[index_j],
        global_important_normal_fluxes_[index_j], global_important_fluxes_[index_j]);

    for (size_t k = 0; k < global_important_indices_[index_j].size(); k++) {
      IndexFirstName.push_back(index_j);
      IndexSecondName.push_back(global_important_indices_[index_j][k]);
    }
  }
}

void PostProcessorFluxMap::ComputeValues(size_t index_j,
                                         std::vector<unsigned int> &local_indices,
                                         std::vector<double> &local_thickness,
                                         std::vector<double> &local_normal_fluxes,
                                         std::vector<double> &local_fluxes) {
  for (size_t j = 0; j < local_indices.size(); j++) {
    if (normal_tags_ == true) {
      if (local_normal_fluxes[j] > 10.) {
        std::setprecision(1);
      } else if (local_normal_fluxes[j] > 1.) {
        std::setprecision(2);
      } else if (local_normal_fluxes[j] > 0.1) {
        std::setprecision(3);
      } else {
        std::setprecision(3);
      }

      ComputedLabelValue.push_back(local_normal_fluxes[j]);
    } else {
      std::setprecision(2);
      ComputedLabelValue.push_back(local_fluxes[j]);
    }
    // Thickness
    double thickness;
    if (logarithmic_thickness_ == false) {
      thickness = 0.5 + 15. * local_thickness[j];
    } else {
      thickness = 0.5 + 5. * std::max(0., 3. + log10(local_thickness[j]));
    }
    ComputedThicknessValue.push_back(thickness);
  }
}
}  // namespace pySMOKEPostProcessor
