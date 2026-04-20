#include "../PostProcessorWrapper_py.h"
#include "../source/ProfilesDatabase.h"
#include "../source/Sensitivities_Surface.h"
//#include "ROPA.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    // TOCHANGE
    const std::string mechanism_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/Surface_Data/kinetics";
    const std::string output_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/Surface_Data/Output";

    ProfilesDatabase profiles_db;
    bool dummy = profiles_db.ReadFileResults(output_folder,true);
    dummy = profiles_db.ReadHeterogeneousKineticMechanism(mechanism_folder,"Surface");
    Sensitivities_Surface sensi;
    bool heterogeneousSensitivity = false;
    const unsigned int NR = 5;

    sensi.SetDatabase(&profiles_db);
    sensi.SetSensitivityType("global");
    sensi.SetOrderingType("peak-values");
    sensi.SetNormalizationType("max-value");
    sensi.SetTarget("CH4");
    // Until here, everything is the same for sensitivity homogeneous and heterogeneous

    // Homogeneous sensitivity analysis
    sensi.Prepare(heterogeneousSensitivity);
    sensi.ReadSensitvityCoefficients();
    sensi.Sensitivity_Analysis(NR);
    std::vector<unsigned int> reactions = sensi.reactions();
    std::vector<double> sensicoeffs = sensi.sensitivityCoefficients();

    std::cout << "Homogeneous Sensitivity coefficients" << std::endl;
    for (unsigned int i = 0; i<sensicoeffs.size(); i++)
        std::cout << sensicoeffs[i] << std::endl;

    std::cout << "Indices" << std::endl;
    for (unsigned int i = 0; i<reactions.size(); i++)
        std::cout << reactions[i] << std::endl;

    // Heterogeneous sensitivity analysis
    heterogeneousSensitivity = true;
    sensi.Prepare(heterogeneousSensitivity);
    sensi.SetNormalizationType("max-value");
    sensi.ReadSensitvityCoefficients();
    sensi.Sensitivity_Analysis(NR);
    std::vector<unsigned int> reactions_het = sensi.reactions();
    std::vector<double> sensicoeffs_het = sensi.sensitivityCoefficients();

    std::cout << "\nHeterogeneous Sensitivity coefficients" << std::endl;
    for (unsigned int i = 0; i<sensicoeffs_het.size(); i++)
        std::cout << sensicoeffs_het[i] << std::endl;
    
    std::cout << "Indices" << std::endl;
    for (unsigned int i = 0; i<reactions.size(); i++)
        std::cout << reactions_het[i] << std::endl;

    return 0;
}