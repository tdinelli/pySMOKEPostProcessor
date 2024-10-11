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

ProfilesDatabase::ProfilesDatabase() {
  is_kinetics_available_ = false;
  is_ropa_enabled_ = false;
  is_sensitivity_enabled_ = false;

  index_density_ = -1;
  index_velocity_ = -1;
  index_mass_flow_rate_ = -1;
}

ProfilesDatabase::~ProfilesDatabase() {}

void ProfilesDatabase::read_kinetic_mechanism(const std::string& folder_name) {
  boost::filesystem::path path_folder_mechanism = folder_name;
  boost::filesystem::path path_mechanism = path_folder_mechanism / "kinetics.xml";

  if (!boost::filesystem::exists(path_folder_mechanism)) {
    std::cerr << "The specified folder does not exist: " + path_folder_mechanism.string()
              << std::endl;
    std::exit(EXIT_FAILURE);
  }
  if (!boost::filesystem::exists(path_mechanism)) {
    std::cerr
        << "The folder of the kinetic mechanism does not contains any kinetics.xml!"
        << std::endl;
    std::exit(EXIT_FAILURE);
  }

  boost::property_tree::ptree ptree;
  boost::property_tree::read_xml((path_mechanism).string(), ptree);

  thermodynamics_map_xml_ =
      std::make_unique<OpenSMOKE::ThermodynamicsMap_CHEMKIN>(ptree, false);
  kinetics_map_xml_ = std::make_unique<OpenSMOKE::KineticsMap_CHEMKIN>(
      *thermodynamics_map_xml_, ptree, false);

  if (thermodynamics_map_xml_->NumberOfSpecies() == omega_.size()) {
    is_ropa_enabled_ = true;
  } else {
    std::cerr << "Output.xml file contains only a subset of the total species in the "
                 "kinetic mechanism"
              << std::endl;
    std::exit(EXIT_FAILURE);
  }

  boost::filesystem::path path_reaction_names =
      path_folder_mechanism / "reaction_names.xml";

  if (!boost::filesystem::exists(path_reaction_names)) {
    std::cerr << "Kinetic folder does not contain the reaction_names.xml file"
              << std::endl;
    std::exit(EXIT_FAILURE);
  }

  boost::property_tree::read_xml((path_reaction_names).string(), ptree);

  std::stringstream stream;
  stream.str(ptree.get<std::string>("opensmoke.reaction-names"));

  reaction_strings_.reserve(kinetics_map_xml_->NumberOfReactions());
  for (size_t j = 0; j < kinetics_map_xml_->NumberOfReactions(); j++) {
    std::string reaction_string;
    stream >> reaction_string;
    reaction_strings_.push_back(reaction_string);
  }

  is_kinetics_available_ = true;
}

void ProfilesDatabase::read_file_results(const std::string& folder_name) {
  boost::filesystem::path path_folder_results_ = folder_name;
  boost::filesystem::path path_results_ = path_folder_results_ / "Output.xml";

  if (!boost::filesystem::exists(path_results_)) {
    std::cerr << "Output folder does not contain the Output.xml file!" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  boost::property_tree::read_xml((path_results_).string(), xml_main_input_);

  // Here we perform the actual reading of the file
  read_xml();

  boost::filesystem::path path_sensitivities =
      path_folder_results_ / "Sensitivities.xml";
  if (boost::filesystem::exists(path_sensitivities)) { is_sensitivity_enabled_ = true; }
}

void ProfilesDatabase::read_xml() {
  // 1. Indices of T, P and MW
  boost::optional<boost::property_tree::ptree&> child =
      xml_main_input_.get_child_optional("opensmoke.t-p-mw");

  if (child) {
    std::stringstream stream;
    stream.str(xml_main_input_.get<std::string>("opensmoke.t-p-mw"));
    stream >> index_T_;
    stream >> index_P_;
    stream >> index_MW_;
  } else {
    std::cerr << "Corrupted xml file: missing the t - p - mw leaf" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  // 2. Additional
  child = xml_main_input_.get_child_optional("opensmoke.additional");

  if (child) {
    std::stringstream stream;
    stream.str(xml_main_input_.get<std::string>("opensmoke.additional"));

    size_t number_of_additional_profiles;
    stream >> number_of_additional_profiles;

    list_additional_.reserve(number_of_additional_profiles);

    for (size_t j = 0; j < number_of_additional_profiles; j++) {
      std::string unit;
      std::string dummy;
      stream >> dummy;
      stream >> unit;
      list_additional_.push_back(dummy + " " + unit);

      if (dummy == "density") { index_density_ = j; }
      if (dummy == "velocity") { index_velocity_ = j; }
      if (dummy == "mass-flow-rate") { index_mass_flow_rate_ = j; }
      if (dummy == "x-coord") { index_x_coord_ = j; }
      if (dummy == "z-coord") { index_z_coord_ = j; }
      if (dummy == "volume") { index_volume_ = j; }

      stream >> dummy;
    }
  } else {
    std::cerr << "Corrupted xml file: missing the additional_ leaf" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  // 3. Species (mass fractions)
  std::vector<std::string> string_list_massfractions_unsorted;
  child = xml_main_input_.get_child_optional("opensmoke.mass-fractions");

  if (child) {
    std::stringstream stream;
    stream.str(xml_main_input_.get<std::string>("opensmoke.mass-fractions"));

    size_t number_of_massfractions_profiles;
    stream >> number_of_massfractions_profiles;

    index_of_massfractions_profiles_.resize(number_of_massfractions_profiles);
    string_list_massfractions_unsorted.reserve(number_of_massfractions_profiles);

    mw_species_.resize(number_of_massfractions_profiles);
    for (size_t j = 0; j < number_of_massfractions_profiles; j++) {
      std::string dummy;
      stream >> dummy;
      string_list_massfractions_unsorted.push_back(dummy);

      stream >> mw_species_[j];
      stream >> index_of_massfractions_profiles_[j];
    }

    string_list_massfractions_sorted_ = string_list_massfractions_unsorted;

    std::sort(string_list_massfractions_sorted_.begin(),
              string_list_massfractions_sorted_.end());
    // string_list_massfractions_sorted_.sort();

    sorted_index_.resize(number_of_massfractions_profiles);
    for (size_t j = 0; j < number_of_massfractions_profiles; j++) {
      for (size_t k = 0; k < number_of_massfractions_profiles; k++) {
        if (string_list_massfractions_sorted_[j] ==
            string_list_massfractions_unsorted[k]) {
          sorted_index_[j] = k;
          break;
        }
      }
    }
  } else {
    std::cerr << "Corrupted xml file: missing the mass-fractions leaf" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  // 4. Read profiles
  omega_.resize(index_of_massfractions_profiles_.size());
  additional_.resize(list_additional_.size());
  child = xml_main_input_.get_child_optional("opensmoke.profiles-size");

  if (child) {
    std::stringstream stream;
    stream.str(xml_main_input_.get<std::string>("opensmoke.profiles-size"));
    stream >> number_of_abscissas_;
    stream >> number_of_ordinates_;
  } else {
    std::cerr << "Corrupted xml file: missing the profiles-size leaf" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  omega_.resize(index_of_massfractions_profiles_.size());
  for (size_t j = 0; j < index_of_massfractions_profiles_.size(); j++) {
    omega_[j].resize(number_of_abscissas_);
  }

  additional_.resize(list_additional_.size());
  for (size_t j = 0; j < list_additional_.size(); j++) {
    additional_[j].resize(number_of_abscissas_);
  }

  child = xml_main_input_.get_child_optional("opensmoke.profiles");
  if (child) {
    std::stringstream stream;
    stream.str(xml_main_input_.get<std::string>("opensmoke.profiles"));

    for (size_t i = 0; i < number_of_abscissas_; i++) {
      for (size_t j = 0; j < list_additional_.size(); j++) {
        stream >> additional_[j][i];
      }
      for (size_t j = 0; j < index_of_massfractions_profiles_.size(); j++) {
        stream >> omega_[j][i];
      }
    }
  } else {
    std::cerr << "Corrupted xml file: missing the profiles leaf" << std::endl;
    std::exit(EXIT_FAILURE);
  }

  sorted_max.resize(string_list_massfractions_sorted_.size());
  for (size_t j = 0; j < index_of_massfractions_profiles_.size(); j++) {
    sorted_max[j] = -1.e100;
    for (size_t i = 0; i < number_of_abscissas_; i++) {
      if (omega_[sorted_index_[j]][i] > sorted_max[j]) {
        sorted_max[j] = omega_[sorted_index_[j]][i];
      }
    }
  }

  // 5. Conversions
  // Note for the manteiner of the future pay attention cause here its easy to
  // incurr in a division by 0, never happend to me but never say never
  for (size_t j = 0; j < index_of_massfractions_profiles_.size(); j++) {
    if (omega_[j][0] > 1e-8) {
      conversion_species_.push_back(j);
      list_additional_.push_back("conversion-" + string_list_massfractions_unsorted[j]);
      std::vector<double> tmp(number_of_abscissas_);
      for (size_t i = 0; i < number_of_abscissas_; i++) {
        tmp[i] = (omega_[j][0] - omega_[j][i]) / omega_[j][0];
      }
      additional_.push_back(tmp);
    }
  }
}

void ProfilesDatabase::species_coarsening(const double threshold) {
  current_sorted_index.resize(0);
  for (size_t k = 0; k < string_list_massfractions_sorted_.size(); k++) {
    if (sorted_max[k] > threshold) { current_sorted_index.push_back(k); }
  }
}

// 0-based
void ProfilesDatabase::reactions_associated_to_species(const size_t index,
                                                       std::vector<size_t>& indices) {
  kinetics_map_xml_->stoichiometry().BuildStoichiometricMatrix();

  for (int k = 0;
       k <
       kinetics_map_xml_->stoichiometry().stoichiometric_matrix_reactants().outerSize();
       ++k) {
    for (Eigen::SparseMatrix<double>::InnerIterator it(
             kinetics_map_xml_->stoichiometry().stoichiometric_matrix_reactants(), k);
         it; ++it)
      if (it.col() == index) { indices.push_back(it.row()); };
  }
  for (int k = 0;
       k <
       kinetics_map_xml_->stoichiometry().stoichiometric_matrix_products().outerSize();
       ++k) {
    for (Eigen::SparseMatrix<double>::InnerIterator it(
             kinetics_map_xml_->stoichiometry().stoichiometric_matrix_products(), k);
         it; ++it)
      if (it.col() == index) indices.push_back(it.row());
  }

  std::sort(indices.begin(), indices.end());
}

void ProfilesDatabase::is_reactant_product(const size_t reaction_index,
                                           double& netStoichiometry) {
  kinetics_map_xml_->stoichiometry().BuildStoichiometricMatrix();

  std::vector<double> reactants_stoich;
  std::vector<double> products_stoich;
  std::vector<double> reactants_indices;
  std::vector<double> products_indices;
  std::vector<double> duplicate_species_indices;

  Eigen::SparseMatrix<double> reactants =
      kinetics_map_xml_->stoichiometry().stoichiometric_matrix_reactants();
  Eigen::SparseMatrix<double> products =
      kinetics_map_xml_->stoichiometry().stoichiometric_matrix_products();

  // TODO
  // Here there is a large room for improvement in terms of computational
  // efficency keep in mind that the loops repeted can be easily condensed
  // into one but I don't have time now
  for (size_t k = 0; k < reactants.outerSize(); ++k) {
    for (Eigen::SparseMatrix<double>::InnerIterator it(reactants, k); it; ++it) {
      if (it.row() == reaction_index) {
        reactants_stoich.push_back(it.value());
        reactants_indices.push_back(it.col());
      }
    }
  }

  for (size_t k = 0; k < products.outerSize(); ++k) {
    for (Eigen::SparseMatrix<double>::InnerIterator it(products, k); it; ++it) {
      if (it.row() == reaction_index) {
        products_stoich.push_back(it.value());
        products_indices.push_back(it.col());
      }
    }
  }

  // Find if some of the species for the selected reactions appears
  // on the both side of the reaction

  // 1. sorting the vectors
  std::sort(reactants_indices.begin(), reactants_indices.end());
  std::sort(products_indices.begin(), products_indices.end());

  // 2. declaring result vector to store the common elements
  std::vector<double> common_species(reactants_indices.size() + products_indices.size());

  // 3. iterator to store return type
  std::vector<double>::iterator it, end;

  end = std::set_intersection(reactants_indices.begin(), reactants_indices.end(),
                              products_indices.begin(), products_indices.end(),
                              common_species.begin());

  for (it = common_species.begin(); it != end; it++) {
    duplicate_species_indices.push_back(*it);
  }

  if (reactants_indices.size() != 1) {
    netStoichiometry = 1;
  } else if (duplicate_species_indices.size() == 1) {
    double idx = duplicate_species_indices[0];
    int pos_r, pos_p;

    std::vector<double>::iterator it_r;
    std::vector<double>::iterator it_p;

    it_r = std::find(reactants_indices.begin(), reactants_indices.end(), idx);
    if (it_r != reactants_indices.end()) { pos_r = it_r - reactants_indices.begin(); }

    it_p = std::find(products_indices.begin(), products_indices.end(), idx);
    if (it_r != products_indices.end()) { pos_p = it_p - products_indices.begin(); }

    netStoichiometry = -reactants_stoich[pos_r] + products_stoich[pos_p];
  } else if (duplicate_species_indices.size() == 0) {
    netStoichiometry = 1;
  } else {
    std::cerr
        << "Something is wrong with the reaction you are asking for! Reaction id: " +
               std::to_string(reaction_index)
        << std::endl;
    std::exit(EXIT_FAILURE);
  }
}

const void ProfilesDatabase::py_wrap(pybind11::module_& m) {
  py::class_<ProfilesDatabase>(m, "ProfilesDatabase")
      .def(py::init<>())
      .def("read_kinetic_mechanism", &ProfilesDatabase::read_kinetic_mechanism,
           py::call_guard<py::gil_scoped_release>())
      .def("read_file_results", &ProfilesDatabase::read_file_results,
           py::call_guard<py::gil_scoped_release>());
}
