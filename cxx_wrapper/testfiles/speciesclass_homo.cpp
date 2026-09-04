#include "../PostProcessorWrapper_py.h"
#include "ProfilesDatabase.h"
#include "SpeciesClasses.h"
#include "maps/Maps_CHEMKIN"

int main(int argc, char** argv)
{
    const std::string mechanism_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/SpeciesClasses/kinetics";
    const std::string output_folder = "/home/lgiardini/pySMOKEPostProcessor/examples/data/SpeciesClasses/Output";

    ProfilesDatabase profiles_db;
    bool dummy = profiles_db.ReadFileResults(output_folder, false);
    dummy = profiles_db.ReadKineticMechanism(mechanism_folder);

    SpeciesClass species_class;
    species_class.SetDatabase(&profiles_db);
    std::cout << "SpeciesClasses available: " << species_class.speciesClassesAvailable() << std::endl;

    const std::vector<std::string> class_names = species_class.classNames();
    for (unsigned int i = 0; i < class_names.size(); i++)
        std::cout << "class " << i << ": " << class_names[i] << std::endl;

    species_class.ElementalDistribution("C", true);
    const std::vector<double> abscissa = species_class.abscissa();
    const std::vector<std::vector<double>> fractions = species_class.elementalFractions();

    std::cout << "\nCarbon fraction by class at the last point (t = " << abscissa.back() << " s):\n";
    double check = 0.;
    for (unsigned int k = 0; k < class_names.size(); k++) {
        const double v = fractions[k].back();
        check += v;
        std::cout << "  " << class_names[k] << " = " << v << std::endl;
    }
    std::cout << "  sum = " << check << " (should be 1)" << std::endl;

    species_class.SetElement("C");
    species_class.SetFluxAnalysisType("destruction");
    species_class.SetLocalValue(0.5);
    species_class.SetDepth(3);
    species_class.SetWidth(5);
    species_class.SetThreshold(1.0);
    species_class.SetCarbonWeighted(true);   // OpenSMOKE carbon-atom throughput (default)

    // seed the graph walk by class name (default mode)
    species_class.SetFluxPerClass(true);
    species_class.SetClassName("C2");
    species_class.FluxByClass();

    const std::vector<std::vector<double>> M = species_class.fluxMatrix();
    std::cout << "\nFull directed class -> class C flux matrix (nonzero entries):\n";
    for (unsigned int i = 0; i < M.size(); i++)
        for (unsigned int j = 0; j < M[i].size(); j++)
            if (M[i][j] != 0.)
                std::cout << "  " << class_names[i] << " -> " << class_names[j] << " : " << M[i][j]
                          << std::endl;

    const std::vector<int> first = species_class.indexFirstClass();
    const std::vector<int> second = species_class.indexSecondClass();
    const std::vector<double> label = species_class.computedLabel();
    std::cout << "\nPruned class-graph edges (seed class C2): " << first.size() << std::endl;
    for (unsigned int e = 0; e < first.size(); e++)
        std::cout << "  " << class_names[first[e]] << " -> " << class_names[second[e]]
                  << " : " << label[e] << " %" << std::endl;

    // same, but seeded from a species instead
    species_class.SetFluxPerClass(false);
    species_class.SetSpecies("C2H2");
    species_class.SetCarbonWeighted(false);
    species_class.FluxByClass();
    std::cout << "\nSeeded from species C2H2, carbon_weighted=false: "
              << species_class.indexFirstClass().size() << " graph edges" << std::endl;

    return 0;
}
