#include <iostream>
#include "PostProcessor.h"

bool VERBOSE = false;

extern "C" __declspec(dllexport) int pyROPAPostProcessor(
    char* kineticFolder,
    char* outputFolder,
    char* specie,
    int command,
    int ropa_type,
    float ropa_local_value,
    float ropa_region_lower_value,
    float ropa_region_upper_value,
    double* coefficients,
    int* reactions,
    int len){

    std::string postprocessorType;

    if (command == 0){
        postprocessorType = "ropa";
    }
    else{
	    return -1;
    }
	
	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	int return_value = PostProcessor.PrepareROPAPython(specie, ropa_type, ropa_local_value, ropa_region_lower_value, ropa_region_upper_value);
	if (return_value != 0){
	    return return_value;
	}
	return PostProcessor.ComputeROPAPython(coefficients, reactions, len);
	
	return 0;
}

extern "C" __declspec(dllexport) int pySensitivityPostProcessor(
	char* kineticFolder,
	char* outputFolder,
	char* specie,
	int command,
	int sensitivity_type,
	int ordering_type,
	int normalization_type,
	float sensitivity_local_value,
	float sensitivity_region_lower_value,
	float sensitivity_region_upper_value,
	double* coefficients,
	int* reactions,
	int len) 
{
	std::string postprocessorType;

	if (command == 0) {
		postprocessorType = "sensitivity";
	}
	else {
		return -1;
	}

	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	int return_value = PostProcessor.PrepareSensitivityPython(specie, sensitivity_type, sensitivity_local_value, sensitivity_region_lower_value, 
															  sensitivity_region_upper_value, normalization_type, ordering_type);
	if (return_value != 0) {
		return return_value;
	}
	return PostProcessor.ComputeSensitivityPython(coefficients, reactions, len);

	return 0;
}

int main() {

	/*
	* Obbligatori: Output Folder | kinetics Folder 
	* (Obbligatori se vuoi sensitivit�: Sensitivity.xml | Sensitivity.T/P.xml |Sensitivity.specie.xml) ste shit le legge da solo nell'output folder
	* 
	* ROPA -> specie
	*		  type: global | local    | region
	*				   /   | localval | upperval & lowerval     
	* SENSITIVITY -> specie
	*                normalization: local    | max
	*				 type: global | local    | region
	*					     /    | localval | upperval & lowerval
	*				 ordering: peakval | area | absolute area
	*/

	// Compulsory 

//	void printHeader();
//	printHeader();
//
//	std::string kineticFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\kinetics";
//	std::string outputFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\Output";
//    std::string postprocessorType = "ropa";
//	kineticFolder = "/Users/edoardo/Downloads";
//	outputFolder = "/Users/edoardo/Downloads";

//    int num = 10;
//    float* coefficients = (float *)malloc(num*sizeof(float));
//    int* reactions = (int *)malloc(num*sizeof(int));

//	edoardo(kineticFolder, outputFolder, "H2", 0, 1, 0, 0, 0, coefficients, reactions, num);

//	for (int i = 0; i < num; i++){
//	    std::cout << reactions[i] << " : " << coefficients[i] << std::endl;
//	}


//	std::cout << " Hello which kind of postprocessing do you want?" << std::endl;
//	std::cin >> postprocessorType;
//	std::cout << " Plese provide the directory for the kinetic mechanism: " << std::endl;
//	std::cin >> kineticFolder;
	// kineticFolder = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\kinetics";
	// std::cout << kineticFolder << std::endl;
//	std::cout << " Plese provide the directory for the results: " << std::endl;
//	std::cin >> outputFolder;
	// outputFolder = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\Output";
	// std::cout <<  outputFolder << std::endl;

//	if (postprocessorType == "ropa" || postprocessorType == "sensitivity")
//	{
//		PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
//		if (postprocessorType == "ropa")
//		{
//			PostProcessor.Prepare();
//			PostProcessor.ComputeROPA();
//		}
//		if (postprocessorType == "sensitivity")
//		{
//			PostProcessor.Prepare();
//			PostProcessor.SensitivityAnalysis();
//		}
//	}
//	else
//	{
//	    if(VERBOSE){
//	        std::cout << " Please select one of the available post-processing type: ropa | sensitivity" << std::endl;
//	    }
//
//		return -1;
//	}
		
	return 0;
}
