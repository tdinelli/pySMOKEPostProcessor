import os
from pySMOKEPostProcessor import FluxByClass
from pySMOKEPostProcessor.plots.heatmaps import plot_heatmap
from pySMOKEPostProcessor.plots.heatmaps import save_fig

import matplotlib.pyplot as plt

base_path = os.getcwd()
kin_xml_fld = os.path.join(base_path, 'data', 'Classes', 'kinetics')
class_groups_fld = os.path.join(base_path, 'data', 'Classes')
plt_fld = os.path.join(base_path, 'Figures')

simul_flds ={
    'example-c6h6' : os.path.join(base_path, 'data', 'Classes', 'simul', 'Output'),
    }


############################
species_list =['C6H6','C6H5','C5H6','C5H5','C6H5OH','C6H5O','C5H4O','C5H5O','C6H4O2','INDENE','C10H8','BIPHENYL']
filter_dcts = [{},{},{}]   # filter according to selected criteria in name
threshs = [1e-2,1e-2,1e-2] # threshold for minimum flux
n_of_rxns = 200            # max n of rxns to consider for flux (default: 100)
sortlists = [['classtype'],['speciestype'],['bimoltype']] # classtype, speciestype, reactiontype, bimoltype (R+R, RSR+RSR, M+M, ETC) # sum if both apply and sort by this criteria

# assign class
fluxbyclass = FluxByClass(kin_xml_fld, class_groups_fld, verbose = False)
# assign flux and process according to selected criteria
for simul_name, simul_fld in simul_flds.items():
    fluxbyclass.process_flux(species_list, simul_fld, ropa_type = 'global')
    for i, sortlist in enumerate(sortlists):
        sortdf = fluxbyclass.sort_and_filter(sortlists[i], filter_dcts[i], threshs[i])
        # plot heatmap
        fig = plot_heatmap(sortdf)
        # save heatmap
        save_fig(fig, plt_fld, sortlist, simul_name)
        
# additional type of classification: filter addition and abstraction reactions
species_list =['C6H6','C6H5','C5H6','C5H5','INDENE','C10H8','BIPHENYL']
filter_dcts = [{'classtype':['ADD', 'HABS']}] # filter according to selected criteria in name
threshs = [1e-3,] # threshold for minimum flux
sortlists = [['classtype','bimoltype']] # classtype, speciestype, reactiontype, bimoltype (R+R, RSR+RSR, M+M, ETC) # sum if both apply and sort by this criteria

# assign class
fluxbyclass = FluxByClass(kin_xml_fld, class_groups_fld, verbose = False)
for simul_name, simul_fld in simul_flds.items():
    fluxbyclass.process_flux(species_list, simul_fld, ropa_type = 'global')
    for i, sortlist in enumerate(sortlists):
        sortdf = fluxbyclass.sort_and_filter(sortlists[i], filter_dcts[i], threshs[i])
        # plot heatmap
        fig = plot_heatmap(sortdf)
        # save heatmap
        save_fig(fig, plt_fld, sortlist, simul_name)
        
# show plots 
plt.show()
        