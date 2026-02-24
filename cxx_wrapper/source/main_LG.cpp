#include "ProfilesDatabase.h"
#include "Sensitivities.h"
#include "Sensitivities_Surface.h"
//#include "ROPA.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    const std::string mechanism_folder = "C:/Users/lgiardini/OpenSMOKE++Suite/examples/OpenSMOKEpp_BatchReactor/04b-sensitivity-isothermal-constantpressure/kinetics";
    const std::string output_folder = "C:/Users/lgiardini/OpenSMOKE++Suite/examples/OpenSMOKEpp_BatchReactor/04b-sensitivity-isothermal-constantpressure/Output";

    // boost::property_tree::ptree ptree;
	// boost::property_tree::read_xml( (mechanism_folder / "kinetics.xml").string(), ptree );
    //OpenSMOKE::ThermodynamicsMap_CHEMKIN* thermoXML = new OpenSMOKE::ThermodynamicsMap_CHEMKIN(ptree);
    //OpenSMOKE::KineticsMap_CHEMKIN* kinXML = new OpenSMOKE::KineticsMap_CHEMKIN(*thermoXML,ptree);

    ProfilesDatabase profiles_db = new ProfilesDatabase();
    bool dummy = profiles_db.ReadKineticMechansim(mechanism_folder);
    dummy = profiles_db.ReadFileResults(output_folder)
    profiles_db.Prepare();

    Sensitivities sensi = new Sensitivities();
    sensi.SetDatabase(profiles_db);
    sensi.SetNormalizationType("max-value");
    sensi.SetSensitivityTipe("global");
    sensi.SetOrderingType("peak-values");
    sensi.SetTarget("CH4");
    sensi.Prepare();
    sensi.SensitivityAnalysis(10);


    return 0;
}