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
	
}

int main() {

	/*
	* Obbligatori: Output Folder | kinetics Folder 
	* (Obbligatori se vuoi sensitività: Sensitivity.xml | Sensitivity.T/P.xml |Sensitivity.specie.xml) ste shit le legge da solo nell'output folder
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

	void printHeader();
	printHeader();

	std::string kineticFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\kinetics";
	std::string outputFolder; // = "C:\\Users\\timot\\OpenSMOKE++Suite\\examples\\OpenSMOKEpp_BatchReactor\\01a-isothermal-constantvolume\\Output";
	std::string postprocessorType;

	std::cout << " Hello which kind of postprocessing do you want?" << std::endl;
	std::cin >> postprocessorType;
	std::cout << " Plese provide the directory for the kinetic mechanism: " << std::endl;
	std::cin >> kineticFolder;
	std::cout << " Plese provide the directory for the results: " << std::endl;
	std::cin >> outputFolder;

	if (postprocessorType == "ropa" || postprocessorType == "sensitivity") 
	{
		PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
		if (postprocessorType == "ropa")
		{
			PostProcessor.Prepare();
			PostProcessor.ComputeROPA();
		}
		if (postprocessorType == "sensitivity") 
		{
			
		}
	}
	else
	{
		std::cout << " Please select one of the available type: ropa | sensitivity" << std::endl;
		return -1;
	}
		
	return 0;
}
