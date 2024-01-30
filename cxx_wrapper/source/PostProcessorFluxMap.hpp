namespace pySMOKEPostProcessor
{
PostProcessorFluxMap::PostProcessorFluxMap(OpenSMOKE::ThermodynamicsMap_CHEMKIN &thermodynamicsMapXML,
                                           OpenSMOKE::KineticsMap_CHEMKIN &kineticsMapXML)
    : OpenSMOKE::FluxAnalysisMap(thermodynamicsMapXML, kineticsMapXML)
{
}

void PostProcessorFluxMap::ComputeFluxAnalysis()
{
    for (unsigned int j = 0; j < list_of_analyzed_species_.size(); j++)
    {
        const unsigned int index_j = list_of_analyzed_species_[j];
        ComputeValues(index_j, global_important_indices_[index_j], global_relative_thickness_[index_j],
                      global_important_normal_fluxes_[index_j], global_important_fluxes_[index_j]);

        for (unsigned int k = 0; k < global_important_indices_[index_j].size(); k++)
        {
            IndexFirstName.push_back(index_j);
            IndexSecondName.push_back(global_important_indices_[index_j][k]);
        }
    }
    /* TO BE REMOVED (Testing only)
      std::cout << IndexFirstName.size() << std::endl;
      std::cout << IndexSecondName.size() << std::endl;
      std::cout << ComputedLabelValue.size() << std::endl;
      std::cout << ComputedThicknessValue.size() << std::endl;
      for (unsigned int i=0;i<ComputedThicknessValue.size();i++)
      {
        std::cout << ComputedThicknessValue[i] << std::endl;
      }
    */
}

void PostProcessorFluxMap::ComputeValues(const unsigned int index_j, std::vector<unsigned int> &local_indices,
                                         std::vector<double> &local_thickness, std::vector<double> &local_normal_fluxes,
                                         std::vector<double> &local_fluxes)
{
    for (unsigned int j = 0; j < local_indices.size(); j++)
    {
        if (normal_tags_ == true)
        {
            if (local_normal_fluxes[j] > 10.)
                std::setprecision(1);
            else if (local_normal_fluxes[j] > 1.)
                std::setprecision(2);
            else if (local_normal_fluxes[j] > 0.1)
                std::setprecision(3);
            else
                std::setprecision(3);

            ComputedLabelValue.push_back(local_normal_fluxes[j]);
        }
        else
        {
            std::setprecision(2);
            ComputedLabelValue.push_back(local_fluxes[j]);
        }
        // Thickness
        double thickness;
        if (logarithmic_thickness_ == false)
            thickness = 0.5 + 15. * local_thickness[j];
        else
            thickness = 0.5 + 5. * std::max(0., 3. + log10(local_thickness[j]));
        ComputedThicknessValue.push_back(thickness);
    }
}
} // namespace pySMOKEPostProcessor
