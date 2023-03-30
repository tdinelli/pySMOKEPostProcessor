from .postprocessor_backend import postprocessor_backend_obj as backend
from .maps.KineticMap import KineticMap
from .maps.OpenSMOKEppXMLFile import OpenSMOKEppXMLFile
from .utilities import get_c_string, list_to_c_array_of_doubles, list_to_c_array_of_ints, c_array_to_list
from ctypes import c_double, c_int
import pandas as pd

def RateOfProductionAnalysis(kinetic_folder: str, output_folder: str,
							species: str, ropa_type: str, local_value: float = 0,
							lower_value: float = 0, upper_value: float = 0,
							number_of_reactions: int = 10):
        
	species = get_c_string(species)
        
	if(ropa_type != 'global' and ropa_type != 'local' and ropa_type != 'region'):
		raise ValueError('Please select one of the available ROPA type: global | local | region')

	ropa_type = get_c_string(ropa_type)
	local_value = c_double(local_value)
	region_lower_value = c_double(lower_value)
	region_upper_value = c_double(upper_value)
	coefficients = list_to_c_array_of_doubles([0]*number_of_reactions)
	reactions = list_to_c_array_of_ints([0]*number_of_reactions)
	num = number_of_reactions
	number_of_reactions = c_int(number_of_reactions)

	kf_ = kinetic_folder
	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)

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

	reaction_names = []
	KineticMap_ = KineticMap(kf_)

	for i in reactions:
		reaction_names.append(KineticMap_.ReactionNameFromIndex(i))

	return coefficients, reactions, reaction_names

def GetReactionRates(kinetic_folder: str, output_folder: str, abscissae_name: str, reaction_name: str):
        
	kin = KineticMap(kinetic_folder)
	out = OpenSMOKEppXMLFile(kineticFolder = kinetic_folder, 
							OutputFolder = output_folder)
        
	valid_x_name = out.additional_variable
	number_of_abscissae = out.npts

	x_axis_name = ''
	for i in valid_x_name:
		if abscissae_name in i:
			x_axis_name = i
        
	if (x_axis_name == ''): raise Exception('The provided name for the x axis is not valid')

	x_axis = out.getProfile(name = x_axis_name)

	reaction_index = kin.ReactionIndexFromName(name = reaction_name)
	reaction_index = c_int(reaction_index)
	reaction_rates = list_to_c_array_of_doubles([0]*number_of_abscissae)
	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)

	f_handle = backend.handle.GetReactionRates
	backend.call(f_handle, 
				kinetic_folder, 
				output_folder,
				reaction_index,
				reaction_rates)
	
	reaction_rates = c_array_to_list(reaction_rates, number_of_abscissae)
	
	return x_axis, reaction_rates

def GetFormationRates(kinetic_folder: str, output_folder: str, species: str, 
				abscissae_name: str, units: str, formation_rate_type: str):
        
	out = OpenSMOKEppXMLFile(kineticFolder = kinetic_folder,
							OutputFolder = output_folder)
        
	valid_x_name = out.additional_variable
	number_of_abscissae = out.npts
	x_axis_name = ''

	for i in valid_x_name:
		if abscissae_name in i:
			x_axis_name = i
        
	if (x_axis_name == ''): raise Exception('The provided name for the x axis is not valid')

	x_axis = out.getProfile(name = x_axis_name)

	if units != 'mole' and units != 'mass':
		raise ValueError('Available units are: mole | mass')

	if formation_rate_type != 'net' and formation_rate_type != 'production' and formation_rate_type != 'destruction' and formation_rate_type != 'characteristic-time':
		raise ValueError('Available types for the formation rate are: net | production | destruction | characteristic-time')

	formation_rates = list_to_c_array_of_doubles([0]*number_of_abscissae)
	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)
	species = get_c_string(species)
	units = get_c_string(units)
	formation_rate_type = get_c_string(formation_rate_type)

	f_handle = backend.handle.GetFormationRates
	backend.call(f_handle, 
				kinetic_folder, 
				output_folder,
				species,
				units,
				formation_rate_type,
				formation_rates)
	
	formation_rates = c_array_to_list(formation_rates, number_of_abscissae)

	return x_axis, formation_rates

def coeffs_to_df(coefficients, indexes, names, type, netflux = True):
	""" turn ROPA/SENS coefficients into dataframe
		sum the fluxes of the equilibrium reactions if netflux option is active
	"""
	if type in ['ROPA', 'SENS']:
		col = type + '-Coeff'
	else:
		raise ValueError('type must be ROPA or SENS')

	dic = {col: coefficients,'Indices-0based': indexes, 'Reaction Name': names}
	df = pd.DataFrame(dic)
	
	if netflux:
		new_df = pd.DataFrame(index = list(set(indexes)), columns = ['abs', col, 'Reaction Name'])
		
		for grp_idx, grp_df in df.groupby('Indices-0based'): 
			new_df.loc[grp_idx][['abs', col, 'Reaction Name']] = [abs(sum(grp_df[col])), sum(grp_df[col]), grp_df['Reaction Name'].iloc[0]]
		
		new_df = new_df.sort_values(by = 'abs', ascending = False)
		# back to df
		df = new_df.reset_index()
    
	return df