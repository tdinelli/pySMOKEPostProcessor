#include "../PostProcessorWrapper_py.h"
#include "ProfilesDatabase.h"
#include "Sensitivities.h"
//#include "ROPA.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    const std::string mechanism_folder = "/home/lgiardini/Mechanisms/Gas_NO_SOOT";
    const std::string output_folder = "/home/lgiardini/SimTesting/BatchHomo/out";

    ProfilesDatabase profiles_db;
    bool dummy = profiles_db.ReadFileResults(output_folder,false);
    dummy = profiles_db.ReadKineticMechanism(mechanism_folder);

    Sensitivities sensi;
    sensi.SetDatabase(&profiles_db);
    sensi.SetSensitivityType("global");
    sensi.SetOrderingType("peak-values");
    sensi.SetNormalizationType("max-value");
    sensi.SetTarget("CH4");
    sensi.Prepare();
    sensi.ReadSensitvityCoefficients();
    sensi.Sensitivity_Analysis(5);
    std::vector<unsigned int> reactions = sensi.reactions();
    std::vector<double> sensicoeffs = sensi.sensitivityCoefficients();
    for (unsigned int i = 0; i<sensicoeffs.size(); i++)
        std::cout << sensicoeffs[i] << std::endl;

    return 0;
}