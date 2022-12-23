import os
from pySMOKEPostProcessor import FluxByClass

base_path = os.getcwd()
kin_xml_fld = os.path.join(base_path, 'data', 'Classes', 'kinetics')
class_groups_fld = os.path.join(base_path, 'data', 'Classes')
plt_fld = os.path.join(base_path, 'Figures')

simul_flds ={
    'example-c6h6' : os.path.join(base_path, 'data', 'Classes', 'simul', 'Output'),
    }


species_list =['C6H6','C6H5','C5H6','C5H5','C6H5OH','C6H5O','C5H4O','C5H5O','C6H4O2','INDENE','C10H8','BIPHENYL']
filter_dcts = [{},{},{}] # filter according to selected criteria in name
threshs = [1e-2,1e-2,1e-2] # threshold for minimum flux
n_of_rxns = 200 # max n of rxns to consider for flux (default: 100)
sortlists = [['classgroup'],['speciestype'],['bimoltype']] # classgroup, speciestype, subclass, bimoltype (R+R, RSR+RSR, M+M, ETC) # sum if both apply and sort by this criteria

# assign class
fluxbyclass = FluxByClass(kin_xml_fld, class_groups_fld)
# assign flux and process according to selected criteria
for simul_name, simul_fld in simul_flds.items():
    fluxbyclass.process_flux(species_list, simul_name, simul_fld, n_of_rxns = n_of_rxns, ropa_type = 'global')
    fluxbyclass.sort_and_filter(sortlists, filter_dcts, threshs, plt_fld)
    
# additional type of classification: filter addition and abstraction reactions
species_list =['C6H6','C6H5','C5H6','C5H5','INDENE','C10H8','BIPHENYL']
filter_dcts = [{'classgroup':['ADD', 'HABS']}] # filter according to selected criteria in name
threshs = [1e-3,] # threshold for minimum flux
sortlists = [['classgroup','bimoltype']] # classgroup, speciestype, subclass, bimoltype (R+R, RSR+RSR, M+M, ETC) # sum if both apply and sort by this criteria

# assign class
fluxbyclass = FluxByClass(kin_xml_fld, class_groups_fld)
for simul_name, simul_fld in simul_flds.items():
    fluxbyclass.process_flux(species_list, simul_name, simul_fld, ropa_type = 'global')
    fluxbyclass.sort_and_filter(sortlists, filter_dcts, threshs, plt_fld)