#include <iostream>
#include "PostProcessor.h"

bool VERBOSE = false;

// Windows extern "C" __declspec(dllexport)
#ifdef _WIN32
extern "C" __declspec(dllexport)
#else
extern "C"
#endif
int pyROPAPostProcessor(
    char* kineticFolder,
    char* outputFolder,
    char* specie,
    int command,
    int ropa_type,
    double ropa_local_value,
    double ropa_region_lower_value,
    double ropa_region_upper_value,
    double* coefficients,
    int* reactions,
    int len)
{

	std::string postprocessorType;

	if (command == 0)
	{
		postprocessorType = "ropa";
	}
	else
	{
		return -1;
	}
	
	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	
	int return_value = PostProcessor.PrepareROPAPython(specie, ropa_type, ropa_local_value, ropa_region_lower_value, ropa_region_upper_value);
	if (return_value != 0)
	{
	    return return_value;
	}
	return PostProcessor.ComputeROPAPython(coefficients, reactions, len);
	
	return 0;
}

#ifdef _WIN32
extern "C" __declspec(dllexport)
#else
extern "C"
#endif
int pySensitivityPostProcessor(
	char* kineticFolder,
	char* outputFolder,
	char* specie,
	int command,
	int sensitivity_type,
	int ordering_type,
	int normalization_type,
	double sensitivity_local_value,
	double sensitivity_region_lower_value,
	double sensitivity_region_upper_value,
	double* coefficients,
	int* reactions,
	int len) 
{
	std::string postprocessorType;
	if (command == 0) 
	{
		postprocessorType = "sensitivity";
	}
	else 
	{
		return -1;
	}

	PostProcessor PostProcessor(postprocessorType, kineticFolder, outputFolder);
	int return_value = PostProcessor.PrepareSensitivityPython(specie, 
				sensitivity_type, 
				sensitivity_local_value, 
				sensitivity_region_lower_value, 
				sensitivity_region_upper_value, 
				normalization_type, 
				ordering_type);
	if (return_value != 0) {
		return return_value;
	}
	return PostProcessor.ComputeSensitivityPython(coefficients, reactions, len);

	return 0;
}

extern "C" const char* GetReactionName(char* kineticFolder, int reactionIndex)
{
	//std::string kineticFolder = "/home/chimica2/tdinelli/sciexpem/SciExpeM_Execution/Execution_4533/kinetics";
	//std::string outputFolder = "/home/chimica2/tdinelli/sciexpem/SciExpeM_Execution/Execution_4533/results/Case0";
	PostProcessor PostProcessor(kineticFolder);
	
	const char *name = PostProcessor.GetName(reactionIndex).c_str();
		
	return name;

}

int main() 
{
	return 0;
}
