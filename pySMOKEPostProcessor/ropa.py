from .postprocessor_backend import postprocessor_backend_obj as backend
from .utilities import get_c_string, list_to_c_array_of_doubles, list_to_c_array_of_ints, c_array_to_list

from ctypes import c_double, c_int

def RateOfProductionAnalysis(species: str, ropa_type: str, local_value: float = 0,
                             lower_value: float = 0, upper_value: float = 0,
                             number_of_reactions: int = 10):
        
		species = get_c_string(species)
        
		if(ropa_type != 'global' and ropa_type != 'global' and ropa_type != 'global'):
			raise ValueError('Please select one of the available ROPA type: global | local | region')
		
		ropa_type = get_c_string(ropa_type)
		local_value = c_double(local_value)
		region_lower_value = c_double(lower_value)
		region_upper_value = c_double(upper_value)
		coefficients = list_to_c_array_of_doubles([0]*number_of_reactions)
		reactions = list_to_c_array_of_ints([0]*number_of_reactions)
		num = number_of_reactions
		number_of_reactions = c_int(number_of_reactions)
		
		kinetic_folder = get_c_string('/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/kinetics')
		output_folder = get_c_string('/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/Output')

		f_handle = backend.handle.RateOfProductionAnalysis
		backend.call(f_handle, 
					kinetic_folder, 
					output_folder, 
                    species, 
                    ropa_type, 
                    local_value, 
                	region_lower_value,
                    region_upper_value, 
                	number_of_reactions, 
                    coefficients, 
                    reactions)
		
		coefficients = c_array_to_list(coefficients, num)
		reactions = c_array_to_list(reactions, num)

		return coefficients, reactions