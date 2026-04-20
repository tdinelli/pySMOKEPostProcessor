#include "../PostProcessorWrapper_py.h"
#include "ProfilesDatabase.h"
#include "ROPA.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    const std::string mechanism_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/ROPA/kinetics";
    const std::string output_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/ROPA/Output";

    ProfilesDatabase profiles_db;
    bool dummy = profiles_db.ReadFileResults(output_folder,false);
    dummy = profiles_db.ReadKineticMechanism(mechanism_folder);

    // Sensitivities sensi;
    // sensi.SetDatabase(&profiles_db);
    // sensi.SetSensitivityType("global");
    // sensi.SetOrderingType("peak-values");
    // sensi.SetNormalizationType("max-value");
    // sensi.SetTarget("CH4");
    // sensi.Prepare();
    // sensi.ReadSensitivityCoefficients();
    // sensi.Sensitivity_Analysis(5);
    // std::vector<unsigned int> reactions = sensi.reactions();
    // std::vector<double> sensicoeffs = sensi.sensitivityCoefficients();
    // for (unsigned int i = 0; i<sensicoeffs.size(); i++)
    //     std::cout << sensicoeffs[i] << std::endl;

    const unsigned int N_rxns = 5;
    std::vector<unsigned int> rxns_indices(N_rxns);
    std::vector<double> rxns_coefficients(N_rxns);

    ROPA ropa;
    ropa.SetDatabase(&profiles_db);
    ropa.SetROPAType("global");
    ropa.SetSpecies("H2");
    ropa.RateOfProductionAnalysis(N_rxns);
    
    rxns_indices = ropa.reactions();
    rxns_coefficients = ropa.coefficients();

    for (unsigned int i = 0; i<N_rxns; i++){
        std::cout << "Reaction index: " << rxns_indices[i] << std::endl;
        std::cout << "Reaction coeff: " << rxns_coefficients[i] << std::endl;
    }

    return 0;
}