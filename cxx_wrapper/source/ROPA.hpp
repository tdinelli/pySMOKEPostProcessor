ROPA::ROPA() {
  ropaType_ = "global";
  kineticFolder_ = "";
  outputFolder_ = "";
  species_ = "";

  localValue_ = 0;
  upperBound_ = 0;
  lowerBound_ = 0;
}

void ROPA::SetROPAType(const std::string& ropaType) {
  if (ropaType != "global" && ropaType != "local" && ropaType != "region") {
    throw std::invalid_argument("Available ROPA types are: global | local | region");
  }
  ropaType_ = ropaType;
}

void ROPA::SetThickness(const std::string& thickness) {
  if (thickness != "absolute" && thickness != "relative") {
    throw std::invalid_argument("Available thickness types are: absolute | relative(%)");
  }
  thickness_ = thickness;
}

void ROPA::SetFluxAnalysisType(const std::string& type) {
  if (type != "production" && type != "destruction") {
    throw std::invalid_argument(
        "Available flux analysis types are: production | destruction");
  }
  flux_type_ = type;
}
void ROPA::SetLabelType(const std::string& type) {
  if (type != "absolute" && type != "relative") {
    throw std::invalid_argument("Available label types are: absolute | relative(%)");
  }
  label_type_ = type;
}

void ROPA::RateOfProductionAnalysis(const unsigned int& number_of_reactions) {
  // Select y variables among the species
  if (std::find(data_->string_list_massfractions_sorted.begin(),
                data_->string_list_massfractions_sorted.end(),
                species_) != data_->string_list_massfractions_sorted.end()) {
    speciesIsSelected = true;
  } else {
    throw std::invalid_argument("Please select one of the available species!");
  }

  unsigned int index_of_species;
  for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++) {
    if (speciesIsSelected == true) {
      if (species_ == data_->string_list_massfractions_sorted[j]) {
        index_of_species = data_->sorted_index[j];
        break;
      }
    }
  }

  OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());

  std::vector<int> reaction_indices;
  std::vector<double> reaction_coefficients;

  // Local Analysis
  if (ropaType_ == "local") {
    unsigned int index = 0;
    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[0][j] >= localValue_) {
        index = j;
        break;
      }
    }
    // Recovers mass fractions
    for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
      omega[k + 1] = data_->omega[k][index];

    // Calculates mole fractions
    double MWmix;
    data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                  omega.GetHandle());

    // Calculates concentrations
    const double P_Pa = data_->additional[data_->index_P][index];
    const double T = data_->additional[data_->index_T][index];
    const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
    Product(cTot, x, &c);

    // Calculates formations rates
    data_->kineticsMapXML->SetTemperature(T);
    data_->kineticsMapXML->SetPressure(P_Pa);
    data_->thermodynamicsMapXML->SetTemperature(T);
    data_->thermodynamicsMapXML->SetPressure(P_Pa);

    data_->kineticsMapXML->KineticConstants();
    data_->kineticsMapXML->ReactionRates(c.GetHandle());

    // Ropa
    OpenSMOKE::ROPA_Data ropa;
    data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

    MergePositiveAndNegativeBars(ropa.production_reaction_indices[index_of_species],
                                 ropa.destruction_reaction_indices[index_of_species],
                                 ropa.production_coefficients[index_of_species],
                                 ropa.destruction_coefficients[index_of_species],
                                 reaction_indices, reaction_coefficients);
  }  // Global | Region
  else {
    unsigned int index_min = 0;
    unsigned int index_max = data_->number_of_abscissas_ - 1;
    if (ropaType_ == "region") {
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
        if (index_max == data_->number_of_abscissas_ - 1)
          index_min = index_max - 1;
        else
          index_max = index_min + 1;
      }
    }

    const double delta =
        data_->additional[0][index_max] - data_->additional[0][index_min];

    std::vector<double> global_production_coefficients;
    std::vector<double> global_destruction_coefficients;
    std::vector<unsigned int> global_production_reaction_indices;
    std::vector<unsigned int> global_destruction_reaction_indices;

    for (unsigned int j = index_min; j < index_max - 1; j++) {
      // Recovers mass fractions
      for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
        omega[k + 1] = data_->omega[k][j];

      // Calculates mole fractions
      double MWmix;
      data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                    omega.GetHandle());

      // Calculates concentrations
      const double P_Pa = data_->additional[data_->index_P][j];
      const double T = data_->additional[data_->index_T][j];
      const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
      Product(cTot, x, &c);

      // Calculates formations rates
      data_->kineticsMapXML->SetTemperature(T);
      data_->kineticsMapXML->SetPressure(P_Pa);
      data_->thermodynamicsMapXML->SetTemperature(T);
      data_->thermodynamicsMapXML->SetPressure(P_Pa);

      data_->kineticsMapXML->KineticConstants();
      data_->kineticsMapXML->ReactionRates(c.GetHandle());

      // Ropa
      OpenSMOKE::ROPA_Data ropa;
      data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

      if (ropa.production_coefficients[index_of_species].size() !=
              ropa.production_reaction_indices[index_of_species].size() ||
          ropa.destruction_coefficients[index_of_species].size() !=
              ropa.destruction_reaction_indices[index_of_species].size()) {
        throw std::invalid_argument("SSS");
      }

      if (j == index_min) {
        global_production_coefficients.resize(
            ropa.production_coefficients[index_of_species].size());
        global_destruction_coefficients.resize(
            ropa.destruction_coefficients[index_of_species].size());
        global_production_reaction_indices =
            ropa.production_reaction_indices[index_of_species];
        global_destruction_reaction_indices =
            ropa.destruction_reaction_indices[index_of_species];
      }

      const double dt = (data_->additional[0][j + 1] - data_->additional[0][j]) / delta;
      for (unsigned int k = 0; k < ropa.production_coefficients[index_of_species].size();
           k++)
        global_production_coefficients[k] +=
            dt * ropa.production_coefficients[index_of_species][k];

      for (unsigned int k = 0; k < ropa.destruction_coefficients[index_of_species].size();
           k++)
        global_destruction_coefficients[k] +=
            dt * ropa.destruction_coefficients[index_of_species][k];
    }

    MergePositiveAndNegativeBars(
        global_production_reaction_indices, global_destruction_reaction_indices,
        global_production_coefficients, global_destruction_coefficients, reaction_indices,
        reaction_coefficients);
  }

  coefficients_.resize(std::min<int>(number_of_reactions, reaction_coefficients.size()));
  reactions_.resize(std::min<int>(number_of_reactions, reaction_coefficients.size()));

  for (int i = 0; i < std::min<int>(number_of_reactions, reaction_coefficients.size());
       i++) {
    coefficients_[i] = reaction_coefficients[i];
    reactions_[i] = reaction_indices[i];
  }
}

void ROPA::FluxAnalysis() {
  // Select y variables among the species
  if (std::find(data_->string_list_massfractions_sorted.begin(),
                data_->string_list_massfractions_sorted.end(),
                species_) != data_->string_list_massfractions_sorted.end()) {
    speciesIsSelected = true;
  } else {
    throw std::invalid_argument("Please select one of the available species!");
  }
  unsigned int index_of_species;
  for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++) {
    if (speciesIsSelected == true) {
      if (species_ == data_->string_list_massfractions_sorted[j]) {
        index_of_species = data_->sorted_index[j];
        break;
      }
    }
  }

  unsigned int index_element;  // = ui.comboBox_Elements->currentIndex();
  std::vector<std::string> elements_names = data_->thermodynamicsMapXML->elements();
  for (unsigned int k = 0; k < elements_names.size(); k++) {
    if (element_ == elements_names[k]) {
      index_element = k;
      break;
    }
  }
  const double n_elements =
      data_->thermodynamicsMapXML->atomic_composition()(index_of_species, index_element);

  if (n_elements == 0.) {
    throw std::invalid_argument(
        "The selected species does not contain the selected element");
  }

  const int max_depth = depth_;
  const int max_width = width_;
  const double min_threshold_percentage = threshold_;

  // Local Analysis (Flux can be done only in when local ropa is available)
  unsigned int index = 0;
  for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
    if (data_->additional[0][j] >= localValue_) {
      index = j;
      break;
    }
  }
  OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble r(data_->kineticsMapXML->NumberOfReactions());

  // Recovers mass fractions
  for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++) {
    omega[k + 1] = data_->omega[k][index];
  }
  // Calculates mole fractions
  double MWmix;
  data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                omega.GetHandle());

  // Calculates concentrations
  const double P_Pa = data_->additional[data_->index_P][index];
  const double T = data_->additional[data_->index_T][index];
  const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
  Product(cTot, x, &c);

  // Calculates formations rates
  data_->kineticsMapXML->SetTemperature(T);
  data_->kineticsMapXML->SetPressure(P_Pa);
  data_->thermodynamicsMapXML->SetTemperature(T);
  data_->thermodynamicsMapXML->SetPressure(P_Pa);

  data_->kineticsMapXML->KineticConstants();
  data_->kineticsMapXML->ReactionRates(c.GetHandle());
  data_->kineticsMapXML->GiveMeReactionRates(r.GetHandle());

  // OpenSMOKE::FluxAnalysisMap flux_analysis(*data_->thermodynamicsMapXML,
  // *data_->kineticsMapXML);
  pySMOKEPostProcessor::PostProcessorFluxMap flux_analysis(*data_->thermodynamicsMapXML,
                                                           *data_->kineticsMapXML);

  bool destruction = false;
  bool relativethickness = false;
  bool labelrelative = false;

  if (flux_type_ == "destruction") destruction = true;

  if (thickness_ == "relative") relativethickness = true;

  if (label_type_ == "relative") labelrelative = true;

  flux_analysis.SetDestructionAnalysis(destruction);
  flux_analysis.SetNormalThickness(relativethickness);
  flux_analysis.SetNormalTags(labelrelative);
  flux_analysis.SetLogarithmicThickness(thicknesslogscale_);
  flux_analysis.SetMaxDepth(max_depth);
  flux_analysis.SetMaxWidth(max_width);
  flux_analysis.SetMinPercentageThreshold(min_threshold_percentage);
  flux_analysis.SetAtom(index_element);
  flux_analysis.SetReactionRates(r.Size(), r.GetHandle());

  std::vector<unsigned int> important_indices;
  important_indices.push_back(index_of_species);
  flux_analysis.GloballyAnalyze(important_indices, 0);
  flux_analysis.CalculateThickness();

  flux_analysis.ComputeFluxAnalysis();

  indexFirstName_ = flux_analysis.IndexFirstName;
  indexSecondName_ = flux_analysis.IndexSecondName;
  computedThickness_ = flux_analysis.ComputedThicknessValue;
  computedLabel_ = flux_analysis.ComputedLabelValue;
}

void ROPA::MergePositiveAndNegativeBars(const std::vector<unsigned int>& positive_indices,
                                        const std::vector<unsigned int>& negative_indices,
                                        const std::vector<double>& positive_coefficients,
                                        const std::vector<double>& negative_coefficients,
                                        std::vector<int>& indices,
                                        std::vector<double>& coefficients) {
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

  for (unsigned int i = 0; i < n; i++)
    if (signum[i] == -1) {
      indices[i] *= -1;
      coefficients[i] *= -1.;
    }
}

void ROPA::GetReactionRates(const std::vector<unsigned int>& reaction_indices,
                            const bool& sum_rates) {
  unsigned int numberOfReactions = reaction_indices.size();
  // Calculate the reaction rates
  {
    sumOfRates_.resize(data_->number_of_abscissas_);
    reactionRates_.resize(numberOfReactions,
                          std::vector<double>(data_->number_of_abscissas_, 1));

    OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble omega(
        data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble r(data_->kineticsMapXML->NumberOfReactions());

    for (unsigned int i = 0; i < data_->number_of_abscissas_; i++) {
      // Recovers mass fractions
      for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
        omega[k + 1] = data_->omega[k][i];

      // Calculate mole fractions
      double MWmix;
      data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                    omega.GetHandle());

      // Calculate concentrations
      const double P_Pa = data_->additional[data_->index_P][i];
      const double T = data_->additional[data_->index_T][i];
      const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
      Product(cTot, x, &c);

      // Calculate reaction rates
      data_->kineticsMapXML->SetTemperature(T);
      data_->kineticsMapXML->SetPressure(P_Pa);
      data_->thermodynamicsMapXML->SetTemperature(T);
      data_->thermodynamicsMapXML->SetPressure(P_Pa);

      // data_->kineticsMapXML->KineticConstants();
      data_->kineticsMapXML->ReactionRates(c.GetHandle());
      data_->kineticsMapXML->GiveMeReactionRates(r.GetHandle());

      if (sum_rates) {
        double sum_rate = 0.;
        for (unsigned int k = 0; k < numberOfReactions; k++) {
          double multiplication_factor = 1;
          // data_->isReactantProduct(reaction_indices[k], multiplication_factor);
          const unsigned int j = reaction_indices[k] + 1;
          sum_rate += multiplication_factor * r[j];
        }
        sumOfRates_[i] = sum_rate;
      } else {
        for (unsigned int k = 0; k < numberOfReactions; k++) {
          double multiplication_factor = 1;
          // data_->isReactantProduct(reaction_indices[k], multiplication_factor);
          const unsigned int j = reaction_indices[k] + 1;
          // reactionRates_[k][i] = multiplication_factor * r[j];
          reactionRates_[k][i] = r[j];
        }
      }
    }
  }
}

void ROPA::GetFormationRates(const std::string& specie, const std::string& units,
                             const std::string& type) {
  if (units != "mass" && units != "mole")
    throw std::invalid_argument("Available Formation Rates units are: mole | mass");

  // As for the Reaction Rates keep in mind that AC allow the plot of
  // several species at the same time now let's stay simple one at the time
  // Select y variables among the species
  OpenSMOKE::OpenSMOKEVector<unsigned int> formation_rates_to_plot;
  const std::string selected_species = specie;

  {
    unsigned int n_selected_species = 1;
    ChangeDimensions(n_selected_species, &formation_rates_to_plot, true);
    for (unsigned int j = 0; j < n_selected_species; j++) {
      for (unsigned int k = 0; k < data_->string_list_massfractions_sorted.size(); k++) {
        if (selected_species == data_->string_list_massfractions_sorted[k]) {
          formation_rates_to_plot[j + 1] = k;
          break;
        }
      }
    }
  }

  // Calculate the formation rates
  {
    formationRates_.resize(data_->number_of_abscissas_);

    OpenSMOKE::OpenSMOKEVectorDouble P(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble D(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble omega(
        data_->thermodynamicsMapXML->NumberOfSpecies());
    OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());

    for (unsigned int i = 0; i < data_->number_of_abscissas_; i++) {
      // Recovers mass fractions
      for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++) {
        omega[k + 1] = data_->omega[k][i];
      }

      // Calculates mole fractions
      double MWmix;
      data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                    omega.GetHandle());

      // Calculates concentrations
      const double P_Pa = data_->additional[data_->index_P][i];
      const double T = data_->additional[data_->index_T][i];
      const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
      Product(cTot, x, &c);

      // Calculates formations rates
      data_->kineticsMapXML->SetTemperature(T);
      data_->kineticsMapXML->SetPressure(P_Pa);
      data_->thermodynamicsMapXML->SetTemperature(T);
      data_->thermodynamicsMapXML->SetPressure(P_Pa);

      data_->kineticsMapXML->KineticConstants();
      data_->kineticsMapXML->ReactionRates(c.GetHandle());
      data_->kineticsMapXML->ProductionAndDestructionRates(P.GetHandle(),
                                                           D.GetHandle());  // kmol/m3/s

      if (type == "characteristic-time") {
        const unsigned k = data_->sorted_index[formation_rates_to_plot[1]] + 1;
        formationRates_[i] = c[k] / (D[k] + 1.e-32);
      } else {
        if (units == "mass") {
          OpenSMOKE::ElementByElementProduct(P.Size(), P.GetHandle(),
                                             data_->thermodynamicsMapXML->MWs().data(),
                                             P.GetHandle());
          OpenSMOKE::ElementByElementProduct(D.Size(), D.GetHandle(),
                                             data_->thermodynamicsMapXML->MWs().data(),
                                             D.GetHandle());
        }

        const unsigned k = data_->sorted_index[formation_rates_to_plot[1]] + 1;
        if (type == "net") {
          formationRates_[i] = P[k] - D[k];
        } else if (type == "production") {
          formationRates_[i] = P[k];
        } else if (type == "destruction") {
          formationRates_[i] = D[k];
        } else {
          throw std::invalid_argument(
              "Available Formation Rates types are: net | production | destruction | "
              "characteristic-time");
        }
      }
    }
  }
}

void ROPA::RateOfProductionAnalysis2D(const unsigned int& number_of_reactions,
                                      const double& local_x, const double& local_z,
                                      const double& region_low_x,
                                      const double& region_up_x,
                                      const double& region_low_z,
                                      const double& region_up_z) {
  // This function is totally inefficent and by far the worst code I have evere written
  // Select y variables among the species
  if (std::find(data_->string_list_massfractions_sorted.begin(),
                data_->string_list_massfractions_sorted.end(),
                species_) != data_->string_list_massfractions_sorted.end()) {
    speciesIsSelected = true;
  } else {
    throw std::invalid_argument("Please select one of the available species!");
  }

  unsigned int index_of_species;
  for (unsigned int j = 0; j < data_->thermodynamicsMapXML->NumberOfSpecies(); j++) {
    if (speciesIsSelected == true) {
      if (species_ == data_->string_list_massfractions_sorted[j]) {
        index_of_species = data_->sorted_index[j];
        break;
      }
    }
  }

  OpenSMOKE::OpenSMOKEVectorDouble x(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble omega(data_->thermodynamicsMapXML->NumberOfSpecies());
  OpenSMOKE::OpenSMOKEVectorDouble c(data_->thermodynamicsMapXML->NumberOfSpecies());

  std::vector<int> reaction_indices;
  std::vector<double> reaction_coefficients;
  // Local Analysis
  if (ropaType_ == "local") {
    unsigned int index = 0;
    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[data_->index_x_coord][j] >= local_x &&
          data_->additional[data_->index_z_coord][j] >= local_z) {
        index = j;
        break;
      }
    }
    // Recovers mass fractions
    for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++) {
      omega[k + 1] = data_->omega[k][index];
    }

    // Calculates mole fractions
    double MWmix;
    data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                  omega.GetHandle());

    // Calculates concentrations
    const double P_Pa = data_->additional[data_->index_P][index];
    const double T = data_->additional[data_->index_T][index];
    const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
    Product(cTot, x, &c);

    // Calculates formations rates
    data_->kineticsMapXML->SetTemperature(T);
    data_->kineticsMapXML->SetPressure(P_Pa);
    data_->thermodynamicsMapXML->SetTemperature(T);
    data_->thermodynamicsMapXML->SetPressure(P_Pa);

    data_->kineticsMapXML->KineticConstants();
    data_->kineticsMapXML->ReactionRates(c.GetHandle());

    // Ropa
    OpenSMOKE::ROPA_Data ropa;
    data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

    MergePositiveAndNegativeBars(ropa.production_reaction_indices[index_of_species],
                                 ropa.destruction_reaction_indices[index_of_species],
                                 ropa.production_coefficients[index_of_species],
                                 ropa.destruction_coefficients[index_of_species],
                                 reaction_indices, reaction_coefficients);
  } else if (ropaType_ == "region") {  // Region
    std::vector<double> global_production_coefficients;
    std::vector<double> global_destruction_coefficients;
    std::vector<unsigned int> global_production_reaction_indices;
    std::vector<unsigned int> global_destruction_reaction_indices;

    unsigned int index_ll;
    unsigned int index_lr;
    unsigned int index_ul;
    unsigned int index_ur;

    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[data_->index_x_coord][j] >= region_low_x &&
          data_->additional[data_->index_z_coord][j] >= region_low_z) {
        index_ll = j;
        break;
      }
    }

    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[data_->index_x_coord][j] >= region_low_x &&
          data_->additional[data_->index_z_coord][j] >= region_up_z) {
        index_ul = j;
        break;
      }
    }

    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[data_->index_x_coord][j] >= region_up_x &&
          data_->additional[data_->index_z_coord][j] >= region_low_z) {
        index_lr = j;
        break;
      }
    }

    for (unsigned int j = 0; j < data_->number_of_abscissas_; j++) {
      if (data_->additional[data_->index_x_coord][j] >= region_up_x &&
          data_->additional[data_->index_z_coord][j] >= region_up_z) {
        index_ur = j;
        break;
      }
    }
    // TODO ADD CHECK on idices
    // if (index_min == index_max)
    // {
    //     if (index_max == data_->number_of_abscissas_ - 1)
    //         index_min = index_max - 1;
    //     else
    //         index_max = index_min + 1;
    // }
    //

    std::vector<double> volume = data_->additional[data_->index_volume];
    double total_volume;
    for (unsigned int i = 0; i < data_->number_of_abscissas_; i++) {
      if (data_->additional[data_->index_x_coord][i] >=
              data_->additional[data_->index_x_coord][index_ll] &&
          data_->additional[data_->index_x_coord][i] <=
              data_->additional[data_->index_x_coord][index_lr]) {
        if (data_->additional[data_->index_z_coord][i] >=
                data_->additional[data_->index_z_coord][index_ll] &&
            data_->additional[data_->index_z_coord][i] <=
                data_->additional[data_->index_z_coord][index_ul]) {
          total_volume += volume[i];
        }
      }
    }

    int counter = 0;

    for (unsigned int i = 0; i < data_->number_of_abscissas_; i++) {
      if (data_->additional[data_->index_x_coord][i] >=
              data_->additional[data_->index_x_coord][index_ll] &&
          data_->additional[data_->index_x_coord][i] <=
              data_->additional[data_->index_x_coord][index_lr]) {
        if (data_->additional[data_->index_z_coord][i] >=
                data_->additional[data_->index_z_coord][index_ll] &&
            data_->additional[data_->index_z_coord][i] <=
                data_->additional[data_->index_z_coord][index_ul]) {
          // Recovers mass fractions
          for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies();
               k++)
            omega[k + 1] = data_->omega[k][i];

          // Calculates mole fractions
          double MWmix;
          data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(
              x.GetHandle(), MWmix, omega.GetHandle());

          // Calculates concentrations
          const double P_Pa = data_->additional[data_->index_P][i];
          const double T = data_->additional[data_->index_T][i];
          const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
          Product(cTot, x, &c);

          // Calculates formations rates
          data_->kineticsMapXML->SetTemperature(T);
          data_->kineticsMapXML->SetPressure(P_Pa);
          data_->thermodynamicsMapXML->SetTemperature(T);
          data_->thermodynamicsMapXML->SetPressure(P_Pa);

          data_->kineticsMapXML->KineticConstants();
          data_->kineticsMapXML->ReactionRates(c.GetHandle());

          // Ropa
          OpenSMOKE::ROPA_Data ropa;
          data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

          if (ropa.production_coefficients[index_of_species].size() !=
                  ropa.production_reaction_indices[index_of_species].size() ||
              ropa.destruction_coefficients[index_of_species].size() !=
                  ropa.destruction_reaction_indices[index_of_species].size()) {
            throw std::invalid_argument("SSS");
          }

          if (counter == 0) {
            global_production_coefficients.resize(
                ropa.production_coefficients[index_of_species].size());
            global_destruction_coefficients.resize(
                ropa.destruction_coefficients[index_of_species].size());
            global_production_reaction_indices =
                ropa.production_reaction_indices[index_of_species];
            global_destruction_reaction_indices =
                ropa.destruction_reaction_indices[index_of_species];
          }

          double integral_contribution = volume[i] / total_volume;

          for (unsigned int k = 0;
               k < ropa.production_coefficients[index_of_species].size(); k++)
            global_production_coefficients[k] +=
                integral_contribution * ropa.production_coefficients[index_of_species][k];

          for (unsigned int k = 0;
               k < ropa.destruction_coefficients[index_of_species].size(); k++)
            global_destruction_coefficients[k] +=
                integral_contribution *
                ropa.destruction_coefficients[index_of_species][k];

          counter += 1;
        }
      }
    }
    MergePositiveAndNegativeBars(
        global_production_reaction_indices, global_destruction_reaction_indices,
        global_production_coefficients, global_destruction_coefficients, reaction_indices,
        reaction_coefficients);
  } else {  // Global
    double tmp = 0;
    unsigned int index_min = 0;
    unsigned int index_max = data_->number_of_abscissas_;

    std::vector<double> volume = data_->additional[data_->index_volume];
    // double total_volume = std::accumulate(volume.begin(), volume.end(), 0.0d);
    double total_volume = 0;
    for (unsigned int i = 0; i < volume.size(); i++) {
      total_volume += volume[i];
    }

    std::vector<double> global_production_coefficients;
    std::vector<double> global_destruction_coefficients;
    std::vector<unsigned int> global_production_reaction_indices;
    std::vector<unsigned int> global_destruction_reaction_indices;

    for (unsigned int j = index_min; j < index_max; j++) {
      // Recovers mass fractions
      for (unsigned int k = 0; k < data_->thermodynamicsMapXML->NumberOfSpecies(); k++)
        omega[k + 1] = data_->omega[k][j];

      // Calculates mole fractions
      double MWmix;
      data_->thermodynamicsMapXML->MoleFractions_From_MassFractions(x.GetHandle(), MWmix,
                                                                    omega.GetHandle());

      // Calculates concentrations
      const double P_Pa = data_->additional[data_->index_P][j];
      const double T = data_->additional[data_->index_T][j];
      const double cTot = P_Pa / PhysicalConstants::R_J_kmol / T;
      Product(cTot, x, &c);

      // Calculates formations rates
      data_->kineticsMapXML->SetTemperature(T);
      data_->kineticsMapXML->SetPressure(P_Pa);
      data_->thermodynamicsMapXML->SetTemperature(T);
      data_->thermodynamicsMapXML->SetPressure(P_Pa);

      data_->kineticsMapXML->KineticConstants();
      data_->kineticsMapXML->ReactionRates(c.GetHandle());

      // Ropa
      OpenSMOKE::ROPA_Data ropa;
      data_->kineticsMapXML->RateOfProductionAnalysis(ropa);

      if (ropa.production_coefficients[index_of_species].size() !=
              ropa.production_reaction_indices[index_of_species].size() ||
          ropa.destruction_coefficients[index_of_species].size() !=
              ropa.destruction_reaction_indices[index_of_species].size()) {
        throw std::invalid_argument("SSS");
      }

      if (j == index_min) {
        global_production_coefficients.resize(
            ropa.production_coefficients[index_of_species].size());
        global_destruction_coefficients.resize(
            ropa.destruction_coefficients[index_of_species].size());
        global_production_reaction_indices =
            ropa.production_reaction_indices[index_of_species];
        global_destruction_reaction_indices =
            ropa.destruction_reaction_indices[index_of_species];
      }

      double integral_contribution = volume[j] / total_volume;

      for (unsigned int k = 0; k < ropa.production_coefficients[index_of_species].size();
           k++)
        global_production_coefficients[k] +=
            integral_contribution * ropa.production_coefficients[index_of_species][k];

      for (unsigned int k = 0; k < ropa.destruction_coefficients[index_of_species].size();
           k++)
        global_destruction_coefficients[k] +=
            integral_contribution * ropa.destruction_coefficients[index_of_species][k];
    }

    MergePositiveAndNegativeBars(
        global_production_reaction_indices, global_destruction_reaction_indices,
        global_production_coefficients, global_destruction_coefficients, reaction_indices,
        reaction_coefficients);
  }

  coefficients_.resize(std::min<int>(number_of_reactions, reaction_coefficients.size()));
  reactions_.resize(std::min<int>(number_of_reactions, reaction_coefficients.size()));

  for (int i = 0; i < std::min<int>(number_of_reactions, reaction_coefficients.size());
       i++) {
    coefficients_[i] = reaction_coefficients[i];
    reactions_[i] = reaction_indices[i];
  }
}
