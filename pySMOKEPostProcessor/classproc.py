import pandas as pd
import os
import numpy as np
import copy

from pySMOKEPostProcessor import postproc
from pySMOKEPostProcessor.maps.KineticMap import KineticMap
from pySMOKEPostProcessor.rxnclass.RxnClassGroups import ReadRxnGroups
from pySMOKEPostProcessor.rxnclass.rxnclass import rxnclass
from pySMOKEPostProcessor.rxnclass.rxnclass import rxnflux
from pySMOKEPostProcessor.plots.heatmaps import plot_heatmap


###################################################################################################
##################################################################################################

class FluxByClass:
    def __init__(self, kin_xml_fld, class_groups_fld):
        """ read the kinetic mechanism and assign classes if available"""

        kinetics = KineticMap(kin_xml_fld)
        kinetics.Classes()
        reactions_all = []
        for i in range(kinetics.NumberOfReactions):

            reaction = {    'index': i+1, 'name': kinetics.reaction_names[i], \
                            'class': kinetics.rxnclass[i+1], 'subclass': kinetics.rxnsubclass[i+1]
                    }
            reactions_all.append(reaction)

        # parse classes
        _, subcl_grp_dct = ReadRxnGroups(
            class_groups_fld, 'rxn_class_groups.txt')
        
        # sort
        rxns_sorted = rxnclass(reactions_all)
        rxns_sorted.assign_class_grp(subcl_grp_dct)
        
        # assign to self
        self.flux_sorted = rxnflux(rxns_sorted.rxn_class_df)
        self.kin_xml_fld = kin_xml_fld
        self.class_groups_fld = class_groups_fld

    def process_flux(self, species_list, simul_name, simul_fld, n_of_rxns = 100, ropa_type = 'global'):
        print('processing simul {}'.format(simul_fld))

        # simul output
        for sp in species_list:
            ropa = postproc(self.kin_xml_fld, simul_fld)
            tot_rop, indexes, _ = ropa.RateOfProductionAnalysis(specie = sp, ropa_type = ropa_type, number_of_reactions = n_of_rxns)
            tot_rop_df = pd.DataFrame(tot_rop, index=np.array(indexes)+1, columns=['flux_{}'.format(sp)], dtype=float)
            tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
            # assign flux
            self.flux_sorted.assign_flux(tot_rop_df)

        self.flux_sorted.sum_fwbw()
        self.simul_name = simul_name
        
    def sort_and_filter(self, sortlists, filter_dcts, threshs, plt_fld):
        # filter rxns
        for i, sortlist in enumerate(sortlists):
            filter_dct = filter_dcts[i]
            rxns_sorted_i = copy.deepcopy(self.flux_sorted)
            THRESH = threshs[i]
            if filter_dct:
                rxns_sorted_i.filter_class(filter_dct)
            # filter flux
            rxns_sorted_i.filter_flux(threshold=THRESH)
            # sum same speciestype-classgroup-subclass together
            sortdf = rxns_sorted_i.sortby(sortlist)
            # drop unsorted cols
            col_names = sortdf.columns
            for col in col_names:
                if 'UNSORTED' in col:
                    sortdf = sortdf.drop(col, axis=1)
            if len(sortlist) > 1:
                criteria_str = '-'.join(sortlist)
            else:
                criteria_str = sortlist[0]
            plotpath = os.path.join(plt_fld, '{}_{}.png'.format(self.simul_name, criteria_str))
            plot_heatmap(sortdf, plotpath)