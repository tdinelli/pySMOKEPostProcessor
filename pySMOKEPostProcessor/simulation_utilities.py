from .postprocessor_backend import postprocessor_backend_obj as backend
from .utilities import get_c_string, list_to_c_array_of_doubles, c_array_to_list

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
