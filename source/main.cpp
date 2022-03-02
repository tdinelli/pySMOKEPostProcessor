#include <iostream>
#include "PostProcessor.h"


void printHeader() {

	std::cout << "" << std::endl;
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
	std::cout << "                   OpenSMOKE NON graphical post processor                    " << std::endl;
	std::cout << "       Based on the original OpenSMOKE postprocessor made by Alberto Cuoci.  " << std::endl;
	std::cout << "             Authors: Timoteo Dinelli <timoteo.dinelli@polimi.it>            " << std::endl;
	std::cout << "                      Edoardo Ramalli <edoardo.ramalli@polimi.it>            " << std::endl;
	std::cout << "                                                                             " << std::endl;
	std::cout << "                           CRECK modeling group                              " << std::endl;
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
	std::cout << "-----------------------------------------------------------------------------" << std::endl;
	
}

bool VERBOSE = false;

extern "C"
int pyPostProcessor(
    char* kineticFolder,
    char* outputFolder,
    char* specie,
    int command,
    int ropa_type,
    float ropa_local_value,
    float ropa_region_lower_value,
    float ropa_region_upper_value,
    float* coefficients,
    int* reactions,
    int len){

    std::string postprocessorType;

    if (command == 0){
        postprocessorType = "ropa";
    }
    else if (command == 1){
        postprocessorType = "sensitivity";
    }
    else{
        if(VERBOSE){
	        std::cout << " Please select one of the available post-processing type: ropa | sensitivity" << std::endl;
	    }
	    return -1;
    }

	if (postprocessorType == "ropa" || postprocessorType == "sensitivity")
	{
		PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);

		if (postprocessorType == "ropa")
		{
			int return_value = PostProcessor.PreparePython(specie, ropa_type, ropa_local_value, ropa_region_lower_value, ropa_region_upper_value);
			if (return_value != 0){
			    return return_value;
			}
			return PostProcessor.ComputeROPAPython(coefficients, reactions, len);
		}
		if (postprocessorType == "sensitivity")
		{
			PostProcessor.Prepare();
			PostProcessor.SensitivityAnalysis();
		}
	}
	else
	{
	    if(VERBOSE){
	        std::cout << " Please select one of the available post-processing type: ropa | sensitivity" << std::endl;
	    }

		return -1;
	}

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

//	std::string kineticFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\kinetics";
//	std::string outputFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\Output";
//
//	kineticFolder = "/Users/edoardo/Library/Mobile Documents/com~apple~CloudDocs/Projects/sciexpem/ChemModels/26";
//	outputFolder = "/Users/edoardo/Desktop/Case0";
//
//    int num = 10;
//    float* coefficients = (float *)malloc(num*sizeof(float));
//    int* reactions = (int *)malloc(num*sizeof(int));
//
//	edoardo(kineticFolder, outputFolder, "H2", 0, 1, 0, 0, 0, coefficients, reactions, num);
//
//	for (int i = 0; i < num; i++){
//	    std::cout << reactions[i] << " : " << coefficients[i] << std::endl;
//	}


//	std::cout << " Hello which kind of postprocessing do you want?" << std::endl;
//	std::cin >> postprocessorType;
//	std::cout << " Plese provide the directory for the kinetic mechanism: " << std::endl;
//	std::cin >> kineticFolder;
//	// kineticFolder = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\kinetics";
//	// std::cout << kineticFolder << std::endl;
//	std::cout << " Plese provide the directory for the results: " << std::endl;
//	std::cin >> outputFolder;
//	// outputFolder = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\04b-sensitivity-isothermal-constantpressure\\Output";
//	// std::cout <<  outputFolder << std::endl;

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
