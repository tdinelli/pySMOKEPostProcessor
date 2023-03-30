from .postprocessor_backend import postprocessor_backend_obj as backend
from .utilities import get_c_string, list_to_c_array_of_doubles, c_array_to_list
from .maps.OpenSMOKEppXMLFile import OpenSMOKEppXMLFile

def GetSimulationINFO(kinetic_folder: str, output_folder: str):

	maximum, minimum, middle = GetSimulationsBoundary(kinetic_folder, output_folder)
	print(f"Computational domain: \n * Lower Bound: {round(minimum,6)}   Upper Bound: {round(maximum, 6)}")
	print(f" * Middle value: {round(middle, 6)}")
	
	out = OpenSMOKEppXMLFile(kineticFolder = kinetic_folder,
                            OutputFolder = output_folder)
	
	print("Available quantities for the abscissae variable:")
	for i in out.additional_variable:
		print(f" * {i}")
	print(" * All the mass fraction of the species inside the scheme (e.g. H2 or O2)")

def GetSimulationsBoundary(kinetic_folder: str, output_folder: str):

	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)

	domain_maximum = list_to_c_array_of_doubles([0])
	domain_minimum = list_to_c_array_of_doubles([0])
	domain_middle = list_to_c_array_of_doubles([0])
	
	f_handle = backend.handle.BoundaryLimits
	backend.call(f_handle, 
				kinetic_folder, 
				output_folder, 
				domain_maximum, 
				domain_minimum, 
				domain_middle)
	
	domain_maximum = c_array_to_list(domain_maximum, 1)[0]
	domain_minimum = c_array_to_list(domain_minimum, 1)[0]
	domain_middle = c_array_to_list(domain_middle, 1)[0]

	return domain_maximum, domain_minimum, domain_middle
