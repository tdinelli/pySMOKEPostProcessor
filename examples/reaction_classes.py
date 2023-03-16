#from os import sys, path
#sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import os
import pySMOKEPostProcessor as pp
import matplotlib.pyplot as plt
import numpy as np

def plot_heatmap(sortdf):
	fig, axes = plt.subplots(figsize = [len(sortdf.columns), len(sortdf.index)])

	image = axes.imshow(sortdf.values, aspect='auto', cmap='RdBu_r', vmin=-1, vmax=1)
    
	axes.set_yticks(np.arange(0, len(sortdf.index)))    
	axes.set_xticks(np.arange(0, len(sortdf.columns)))
    
	size_for_lbl = 'xx-large' * (len(sortdf.index) > 3) + 'medium' * (len(sortdf.index) <= 3)

	axes.set_yticklabels([idx.split('flux_')[1] for idx in sortdf.index], fontsize=size_for_lbl)
	axes.set_xticklabels(sortdf.columns, rotation=90, fontsize=size_for_lbl)
    
	plt.colorbar(image)
	fig.tight_layout()
	return fig

# Only for dev purposes
#import os.path
#if os.path.isdir("/Users/tdinelli/"):
#	pp.load("/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib")

base_path = os.getcwd()
kineticFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/Classes/kinetics"
class_group_definition = os.path.join(base_path, 'data', 'Classes')
plt_fld = os.path.join(base_path, 'Figures')


simulations_output ={'example-c6h6' : "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/Classes/simul/Output"}

species_list =['C6H6','C6H5','C5H6','C5H5','C6H5OH','C6H5O','C5H4O','C5H5O','C6H4O2','INDENE','C10H8','BIPHENYL']
filter_dcts = [{},{},{}]   # filter according to selected criteria in name
threshs = [1e-2,1e-2,1e-2] # threshold for minimum flux
n_of_rxns = 200            # max n of rxns to consider for flux (default: 100)
sortlists = [['classtype'],['speciestype'],['bimoltype']] # classtype, speciestype, reactiontype, bimoltype (R+R, RSR+RSR, M+M, ETC) 
                                                          # sum if both apply and sort by this criteria

# assign class
fluxbyclass = pp.FluxByClass(kinetic_mechanism = kineticFolder, 
			    			classes_definition = class_group_definition, 
							verbose = False)

# assign flux and process according to selected criteria
for simul_name, simul_fld in simulations_output.items():
	fluxbyclass.process_flux(species_list = species_list, results_folder = simul_fld, ropa_type = 'global')
	for i, sortlist in enumerate(sortlists):
		sortdf = fluxbyclass.sort_and_filter(sortlists[i], filter_dcts[i], threshs[i])
		if not sortdf.empty:
			plot_heatmap(sortdf)
			plt.show()


# additional type of classification: filter addition and abstraction reactions
species_list =['C6H6','C6H5','C5H6','C5H5','INDENE','C10H8','BIPHENYL']
filter_dct = {'classtype':['ADD', 'HABS']} # filter according to selected criteria in name
thresh = 1e-3 # threshold for minimum flux
sortlist = ['classtype','bimoltype'] # classtype, speciestype, subclass, bimoltype (R+R, RSR+RSR, M+M, ETC) 
                                     # sum if both apply and sort by this criteria

# assign class
fluxbyclass = pp.FluxByClass(kinetic_mechanism = kineticFolder, 
			    			classes_definition = class_group_definition, 
							verbose = False)

# assign flux and process according to selected criteria
for simul_name, simul_fld in simulations_output.items():
	fluxbyclass.process_flux(species_list = species_list, results_folder = simul_fld, ropa_type = 'global')
	for i, sortlist in enumerate(sortlists):
		sortdf = fluxbyclass.sort_and_filter(sortlists[i], filter_dcts[i], threshs[i])
		if not sortdf.empty:
			plot_heatmap(sortdf)
			plt.show()