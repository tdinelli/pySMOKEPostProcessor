from .postprocessor_backend import postprocessor_backend_obj as backend
from .utilities import get_c_string, list_to_c_array_of_doubles, list_to_c_array_of_ints, c_array_to_list
from .graph_writer import GraphWriter
from .maps.KineticMap import KineticMap
from ctypes import c_bool, c_int, c_double

def FluxAnalysis(kinetic_folder: str, output_folder: str, 
				species: str, element: str, flux_analysis_type: str,
                thickness: str, thickness_log_scale: bool,
                label_type: str, depth: int = 2, width: int = 5,
                threshold: float = 0, local_value: float = 0.01):
        
	species = get_c_string(species)
	element = get_c_string(element)

	if(flux_analysis_type != 'production' and  flux_analysis_type != 'destruction'):
		raise ValueError("The available type for the flux analysis are: production | destruction")

	if(thickness != 'absolute' and thickness != 'relative'):
		raise ValueError("The available type for the caluclation of the thicknsss are: absolute | relative(%)")

	if(label_type != 'absolute' and label_type != 'relative'):
		raise ValueError("The available type for the labeling are: absolute | relative(%)")

	flux_analysis_type = get_c_string(flux_analysis_type)
	thickness = get_c_string(flux_analysis_type)
	label_type = get_c_string(label_type)
	kinetic_folder = get_c_string(kinetic_folder)
	output_folder = get_c_string(output_folder)

	thickness = c_bool(thickness_log_scale)
	depth = c_int(depth)
	width = c_int(width)
	threshold = c_double(threshold)
	local_value = c_double(local_value)

	indexFirstName = list_to_c_array_of_ints([0]*1000)
	indexSecondName = list_to_c_array_of_ints([0]*1000)
	computedThickness = list_to_c_array_of_doubles([0]*1000)
	computedLabel = list_to_c_array_of_doubles([0]*1000)
	length = list_to_c_array_of_ints([0]*1000)

	f_handle = backend.handle.FluxAnalysis
	backend.call(f_handle, 
				kinetic_folder, 
				output_folder,
				species,
				element,
				flux_analysis_type,
				local_value,
				thickness,
				thickness_log_scale,
				label_type,
				depth,
				width,
				threshold,
				indexFirstName,
				indexSecondName,
				computedThickness,
				computedLabel,
				length)
	
	length = c_array_to_list(length)[0]
	indexFirstName = c_array_to_list(indexFirstName, length)
	indexSecondName = c_array_to_list(indexSecondName, length)
	computedThickness = c_array_to_list(computedThickness, length)
	computedLabel = c_array_to_list(computedLabel, length)

	firstNames = []
	secondNames = []
	KineticMap_ = KineticMap(kinetic_folder.decode("utf-8"))

	for j in range(len(indexFirstName)):
		firstNames.append( KineticMap_.SpecieNameFromIndex(indexFirstName[j]))
		secondNames.append(KineticMap_.SpecieNameFromIndex(indexSecondName[j]))

	Graph = GraphWriter(flux_analysis_type)
	Graph = Graph.CreateGraph(firstNames, secondNames, computedThickness, computedLabel)

	return Graph