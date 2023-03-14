from .postprocessor_backend import postprocessor_backend_obj as backend
from .utilities import get_c_string, list_to_c_array_of_doubles, list_to_c_array_of_ints, c_array_to_list
from ctypes import c_double, c_int

def SensitivityAnalysis(kinetic_folder: str, output_folder: str,
						target: str, sensitivity_type: str, ordering_type: str,
                    	normalization_type: str, local_value: float = 0,
                        lower_value: float = 0, upper_value: float = 0,
                        number_of_reactions: int = 10):
    
	target = get_c_string(target)
    
	if (sensitivity_type != 'global' and sensitivity_type != 'local' and sensitivity_type != 'region'):
		raise ValueError('Please select one of the available Sensitivity analysis type global | local | region')

	if (ordering_type != 'peak_value' and ordering_type != "area" and ordering_type != "absolute_area"):
		raise ValueError('Please select one of the available ordering type: peak_value | area | absolute_area')

	if (normalization_type != 'local' and normalization_type != 'max_value'):
		raise ValueError('Please select one of the available normalization: local | max_value')

	sensitivity_type = get_c_string(sensitivity_type)
	ordering_type = get_c_string(ordering_type)
	normalization_type = get_c_string(normalization_type)

	local_value = c_double(local_value)
	region_lower_value = c_double(lower_value)
	region_upper_value = c_double(upper_value)
	
	coefficients = list_to_c_array_of_doubles([0]*number_of_reactions)
	reactions = list_to_c_array_of_ints([0]*number_of_reactions)
	
	num = number_of_reactions
	number_of_reactions = c_int(number_of_reactions)
	
	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)
	
	f_handle = backend.handle.SensitivityAnalysis
	backend.call(f_handle, 
				kinetic_folder, 
				output_folder,
				target,
				sensitivity_type,
				ordering_type,
				normalization_type,
				local_value,
				region_lower_value,
				region_upper_value,
				number_of_reactions,
				coefficients,
				reactions)
	
	coefficients = c_array_to_list(coefficients, num)
	reactions = c_array_to_list(reactions, num)

	return coefficients, reactions