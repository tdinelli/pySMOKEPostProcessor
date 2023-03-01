import pandas as pd
import numpy as np
import copy

from pySMOKEPostProcessor import postproc
from pySMOKEPostProcessor.maps.KineticMap import KineticMap
from pySMOKEPostProcessor.rxnclass.RxnClassGroups import ReadRxnGroups
from pySMOKEPostProcessor.rxnclass.rxnclass import rxnclass
from pySMOKEPostProcessor.rxnclass.rxnclass import rxnflux

###################################################################################################

class FluxByClass:

    def __init__(self, kinetic_mechanism, classes_definition, verbose: bool):
        """read the kinetic mechanism and assign classes if available"""

        kinetics = KineticMap(kinetic_mechanism)
        kinetics.Classes()
        reactions_all = []
        for i in range(kinetics.NumberOfReactions):

            reaction = {'index': i+1, 
                        'name': kinetics.reaction_names[i], 
                        'class': kinetics.rxnclass[i+1], 
                        'reactiontype': kinetics.rxnsubclass[i+1]}

            reactions_all.append(reaction)

        # parse classes
        _, subcl_grp_dct = ReadRxnGroups(classes_definition, 'rxn_class_groups.txt')

        # sort
        rxns_sorted = rxnclass(reactions_all, verbose=False)
        rxns_sorted.assign_class_grp(subcl_grp_dct)

        # assign to self
        self.flux_sorted = rxnflux(rxns_sorted.rxn_class_df, verbose)
        self.kinetic_mechanism = kinetic_mechanism
        self.classes_definition = classes_definition
        self.verbose = verbose

    def process_flux(self, 
                    species_list,
                    results_folder, 
                    n_of_rxns = 100,
                    ropa_type = 'global'):
        
        if self.verbose:
            print('processing simul {}'.format(results_folder))

        # distinguish pp input based on ropa type
        loc_low_up = np.array([0, 0, 0,], dtype = float)
        if isinstance(ropa_type, dict):
            if 'local' in ropa_type.keys():
                loc_low_up[0] = ropa_type['local']
                ropa_type = 'local'
            elif 'region' in ropa_type.keys():
                loc_low_up[1:] = ropa_type['region']
                ropa_type = 'region'
            
        # simul output
        for sp in species_list:
            pp = postproc(self.kinetic_mechanism, results_folder)
            tot_rop, indexes, _ = pp.RateOfProductionAnalysis(specie = sp, ropa_type = ropa_type, local_value = loc_low_up[0],
                                 lower_value = loc_low_up[1], upper_value = loc_low_up[2], number_of_reactions = n_of_rxns)
            tot_rop_df = pd.DataFrame(tot_rop, index=np.array(indexes)+1, columns=['flux_{}'.format(sp)], dtype=float)
            tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
            # assign flux
            self.flux_sorted.assign_flux(tot_rop_df)

        self.flux_sorted.sum_fwbw()
        
    def sort_and_filter(self, sortlist, filter_dct, thresh):
        # filter rxns
        rxns_sorted = copy.deepcopy(self.flux_sorted)
        if filter_dct:
            rxns_sorted.filter_class(filter_dct)
        # filter flux
        rxns_sorted.filter_flux(threshold=thresh)
        # sum same speciestype-classgroup-reactiontype together
        sortdf = rxns_sorted.sortby(sortlist)
        # drop unsorted cols
        col_names = sortdf.columns
        for col in col_names:
            if 'UNSORTED' in col:
                sortdf = sortdf.drop(col, axis=1)

        return sortdf