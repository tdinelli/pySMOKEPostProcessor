#include "../PostProcessorWrapper_py.h"
#include "ProfilesDatabase.h"
#include "ROPA_Surface.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    const std::string mechanism_folder = "/home/lgiardini/SimTesting/BatchHet/CVD_NO_SOOT";
    const std::string output_folder = "/home/lgiardini/SimTesting/BatchHet/out";

    ProfilesDatabase profiles_db;
    bool dummy = profiles_db.ReadFileResults(output_folder,true);
    dummy = profiles_db.ReadHeterogeneousKineticMechanism(mechanism_folder,"Surface");

    const unsigned int N_rxns = 5;
    std::vector<unsigned int> rxns_indices(N_rxns);
    std::vector<double> rxns_coefficients(N_rxns);
    std::vector<unsigned int> het_rxns_indices(N_rxns);
    std::vector<double> het_rxns_coefficients(N_rxns);

    ROPA_Surface ropa;
    ropa.SetDatabase(&profiles_db);
    ropa.SetROPAType("global");
    ropa.SetLocalValue(0.5);
    ropa.SetSpecies("CH4");
    ropa.RateOfProductionAnalysis(N_rxns);
    
    rxns_indices = ropa.reactions();
    rxns_coefficients = ropa.coefficients();

    std::cout << "Homogeneous reactions " << std::endl;
    for (unsigned int i = 0; i<N_rxns; i++){
        std::cout << "Reaction index: " << rxns_indices[i] << std::endl;
        std::cout << "Reaction coeff: " << rxns_coefficients[i] << std::endl;
    }

    het_rxns_indices = ropa.reactions_surface();
    het_rxns_coefficients = ropa.coefficients_surface();

    std::cout << "Heterogeneous reactions " << std::endl;
    for (unsigned int i = 0; i<N_rxns; i++){
        std::cout << "Reaction index: " << het_rxns_indices[i] << std::endl;
        std::cout << "Reaction coeff: " << het_rxns_coefficients[i] << std::endl;
    }

    return 0;
}