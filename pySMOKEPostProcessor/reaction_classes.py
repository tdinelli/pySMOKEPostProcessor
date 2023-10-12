import pandas as pd
import numpy as np
import copy
from operator import add, neg

from .reaction_classes_utilities.reaction_classes_groups import ReadReactionsGroups
from .reaction_classes_utilities.reaction_classes import reaction_classes
from .reaction_classes_utilities.reaction_classes import reaction_fluxes


class FluxByClass:

    def __init__(self, kinmap, classes_definition, verbose: bool = False):
        """
        read the kinetic mechanism and assign classes if available
        kinmap: kinetic map already processed
        """
        kinmap.Classes()
        reactions_all = []
        for i in range(kinmap.NumberOfReactions):
            reaction = {
                'index': i+1,
                'name': kinmap.reaction_names[i],
                'class': kinmap.rxnclass[i+1],
                'reactiontype': kinmap.rxnsubclass[i+1]
            }
            reactions_all.append(reaction)

        # parse classes
        _, subcl_grp_dct = ReadReactionsGroups(classes_definition)
        # sort
        rxns_sorted = reaction_classes(reactions_all, verbose=False)
        rxns_sorted.assign_class_grp(subcl_grp_dct)

        # assign to self
        self.rxns_sorted = rxns_sorted
        # was put for cumulative rxn rates # self.flux_sorted = reaction_fluxes(rxns_sorted.rxn_class_df, verbose) # needed for cumulative reaction rates - but should be removed
        self.classes_definition = classes_definition
        self.verbose = verbose
        self.kinetic_map = kinmap
        self.reactions_all = reactions_all

    def process_flux(self, species_list, tot_rop_dct):
        # input tot_rop_dct: dictionary with ROPA performed for a set of species {spc: {ropa dct}}
        # reinitialize
        self.flux_sorted = reaction_fluxes(self.rxns_sorted.rxn_class_df, self.verbose)

        # add fluxes
        for species in species_list:
            if isinstance(species, str):
                sps = [species]
                spname = species
            elif isinstance(species, dict):
                spname = list(species.keys())[0]
                sps = species[spname]
   
            tot_rop_df = None
            for sp in sps:
                tot_rop_df0 = pd.DataFrame(tot_rop_dct[sp]['coefficients'], index=np.array(tot_rop_dct[sp]['reaction_indices'])+1, 
                                           columns=['flux_{}'.format(spname)], dtype=float)
                tot_rop_df0 = tot_rop_df0.groupby(level=0).sum() # sum rxns with same indexes
    
                if isinstance(tot_rop_df, pd.DataFrame):
                    # concatenate
                    tot_rop_df = pd.concat([tot_rop_df, tot_rop_df0])
                    tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
                else:
                    tot_rop_df = copy.deepcopy(tot_rop_df0)			

                # Luna: nego - ho controllato e mi sembra a posto
                # check and ask luna why first row of tot_rop_df contains the first reaction 
                # of the kinetic model even if it does not include the selected species
                
            # concatenate flux to the dataframe of rxn classes
            self.flux_sorted.assign_flux(tot_rop_df)

        self.flux_sorted.sum_fwbw()

    def sort_and_filter(self, 
                        sortlist, 
                        filter_dct: dict = {}, 
                        thresh: float = 1e-3, 
                        weigh: str = 'false'):
        # weight options: normbyspecies, omegaij, false
        # filter rxns
        rxns_sorted = copy.deepcopy(self.flux_sorted)
        if len(filter_dct) > 0:
            rxns_sorted.filter_class(filter_dct)
        # filter flux
        rxns_sorted.filter_flux(threshold=thresh)
        # sum same speciestype-classgroup-reactiontype together
        sortdf = rxns_sorted.sortby(sortlist, weigh = weigh)

        return sortdf

    # new function to compute and plot reaction class rate profiles along axial coordinate
    def process_reaction_class_rate(self, results_folder: str, x_axis_name: str, reactionclass_type: str):
        # to be extended to all types (reactiontype, classtype, speciestype, bimoltype. requires a call to sort_and_filter first)
        # do it similar to sort_and_filter, with sortlist (which only provides criteria for getting the rates) and filter_dct
        indici = [i['index']-1 for i in self.reactions_all if not i['reactiontype'] == None if reactionclass_type in i['reactiontype']]
        # versione precedente: era in ropa.py (ora tutto in postprocessor.py)
        x_axis, reaction_rate_ = GetReactionRatesIndex(kinetic_folder=self.kinetic_mechanism,
                                                       output_folder=results_folder,
                                                       reaction_index=indici,
                                                       abscissae_name=x_axis_name)
		
        return x_axis, reaction_rate_
	
    # new function to compute plot cumulative contribution of different reactions
    # to production/consumption rate profile of a species
    def process_cumulative_reaction_rate(self, results_folder: str,
                                         x_axis_name: str,
                                         species: str, 
                                         n_of_rxns: int, 
                                         rate_type: str,
                                         filter_ClassesToPlot: list,
                                         threshold: float):

        # distinguish pp input based on ropa type
        loc_low_up = np.array([0, 0, 0, ], dtype=float)
        tot_rop_df = None

        tot_rop, indexes, _ = RateOfProductionAnalysis(kinetic_folder=self.kinetic_mechanism, 
                                                       output_folder=results_folder, 
                                                       species = species, 
                                                       ropa_type = 'global', 
                                                       local_value = loc_low_up[0],
                                                       lower_value = loc_low_up[1], 
                                                       upper_value = loc_low_up[2], 
                                                       number_of_reactions = n_of_rxns)

        tot_rop_df0 = pd.DataFrame(tot_rop, index=np.array(indexes)+1, columns=['flux_' + species], dtype=float)
        tot_rop_df0 = tot_rop_df0.groupby(level=0).sum() # sum rxns with same indexes
        # THIS IS CODE REPETITION REMOVE
        if isinstance(tot_rop_df, pd.DataFrame):
            # concatenate
            tot_rop_df = pd.concat([tot_rop_df, tot_rop_df0])
            tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
        else:
            tot_rop_df = copy.deepcopy(tot_rop_df0)			
            # assign flux
            # self.flux_sorted.assign_flux(tot_rop_df)
        # TODO		
        self.flux_sorted.sum_fwbw() # some errors to be fixed. Ask Luna

        tot_rop_pos_df = tot_rop_df[(tot_rop_df >= 0).all(axis=1)]
        tot_rop_sorted_pos_df = tot_rop_pos_df.sort_values(by = 'flux_' + species, axis=0, ascending=False)

        tot_rop_neg_df = tot_rop_df[(tot_rop_df < 0).all(axis=1)]
        tot_rop_sorted_neg_df = tot_rop_neg_df.sort_values(by = 'flux_' + species, axis=0, ascending=True)

        indici_production = [tot_rop_sorted_pos_df.index[i] for i in range(len(tot_rop_sorted_pos_df))]
        indici_consumption = [tot_rop_sorted_neg_df.index[i] for i in range(len(tot_rop_sorted_neg_df))]
		
        print(tot_rop_df)

        if rate_type == 'P':
            indici = indici_production
        elif rate_type == 'C':
            indici = indici_consumption
        else:
            raise TypeError('rate_type can be only "P" (production) or "C" (consumption)')
		
        reaction_rate_all = []
        matrix_of_rates_all = []
        matrix_of_rates = []
        rate_percentage_contribution = []
        nomi = []

        print(indici)
        for i in range(len(indici)):
            # INVECE DI CHIAMARE QUESTO, PRENDI DIRETTAMENETE GLI INDICI DELLA ROPA
            # CHE DOVREBBERO ESSERE UGUALI. E POI CHIAMA GETREACTIONRATES
            x_axis, reaction_rate_ = GetReactionRatesIndex(kinetic_folder=self.kinetic_mechanism, 
                                                           output_folder=results_folder, 
                                                           reaction_index=[indici[i]-1], 
                                                           abscissae_name=x_axis_name)
			
            nome = self.kinetic_map.ReactionNameFromIndex(indici[i]-1) # nome della reazione
            # TODO
            # to manage equilibrium reaction where 'species' can be on the right or on the left of '=' 
            # i.e., consistently if they are produced or consumed in a specific simulation
            # REFACTORING NEEDED IMMEDIATASUBITO
            if not "=>" in nome:
                reagenti = nome.split(':')[-1].split('=')[0]
                prodotti = nome.split(':')[-1].split('=')[-1]
                if rate_type == 'P':
                    if(species in reagenti):
                        reaction_rate_ = list( map(neg, reaction_rate_))
                elif rate_type == 'C':
                    if(species in prodotti):
                        reaction_rate_ = list( map(neg, reaction_rate_))

            # to plot reactions only in specific reaction class
            ToPlot = 1
            if len(filter_ClassesToPlot) >= 1:
                ToPlot = 0
                for j in range(len(filter_ClassesToPlot)):
                    indici_ToPlot = [k['index']-1 for k in self.reactions_all if not k['reactiontype'] == None if filter_ClassesToPlot[j] in k['reactiontype']]
                    if indici[i] in indici_ToPlot:
                        ToPlot = ToPlot + 1
                if ToPlot == 0:
                    reaction_rate_ = [0] * len(reaction_rate_)

            if ToPlot == 1:
                nomi.append(self.kinetic_map.ReactionNameFromIndex(indici[i]-1)[:30])
                matrix_of_rates_all.append(reaction_rate_)
                if len(nomi) == 1:
                    reaction_rate_all = reaction_rate_
                else:
                    reaction_rate_all = list( map(add, reaction_rate_all, reaction_rate_))
				
        nomi_ret = []
        total_rate_area = np.trapz(y = reaction_rate_all, x = x_axis)
        for i in range(len(nomi)):
            single_rate_area = np.trapz(y = matrix_of_rates_all[i], x = x_axis)
            rate_percentage_contribution.append(single_rate_area / total_rate_area * 100)	
            if rate_percentage_contribution[-1] > threshold:
                nomi_ret.append(nomi[i] + ' ' + str(round(rate_percentage_contribution[-1],1))+ ' %')
                matrix_of_rates.append(matrix_of_rates_all[:][i])
            else:
                rate_percentage_contribution.pop(-1)

        print(rate_percentage_contribution)
        return x_axis, matrix_of_rates, nomi_ret

def merge_maps_byspecies(sorted_dfs_dct):
    """ 
    combines the heatmaps of different simulations for the same set of species and puts them in a new dataframe
    Args:
        sorted_dfs ({idx: dataframe}): sorted dataframes with fluxes.
    
    """
    # simul names
    sim_names = sorted_dfs_dct.keys()
    species_lists = np.concatenate([np.array(sorted_dfs_dct[sim_name].index) for sim_name in sim_names])
    classes_list = np.concatenate([np.array(sorted_dfs_dct[sim_name].columns) for sim_name in sim_names])
    # find common species and classes
    all_sp = np.array(list(set(species_lists)))
    all_cl = np.sort(np.array(list(set(classes_list))))
    # for each species: rename according to simulation name and concatenate dataframes
    dftot = pd.DataFrame(columns = all_cl)
    for sim_name, dffull in sorted_dfs_dct.items():
        # filter indexes
        pdnew = dffull.loc[all_sp]
        # rename indexes according to simul name
        pdnew = pdnew.rename(index = lambda spname: spname + '-' + str(sim_name))
        # now concate to dftot
        dftot = pd.concat([dftot, pdnew])
  
    # replace nan with 0
    dftot = dftot.replace(np.nan, 0)
    # order according to index, so you have all species in rows
    dftot = dftot.sort_index()
 
    return dftot
 

def FDI(sorted_dfs_dct: dict, 
        fditype: str = 'global',
        speciesi: str = '',
        classj: str = ''):
    """ 
    computes FDIs for a given set of flames
    see https://doi.org/10.1016/j.combustflame.2022.112073
    
    Args:
        sorted_dfs ({idx: dataframe}): sorted dataframes with fluxes.
        fditype : global (sum over ij), species (sum over j), class (sum over i)
        speciesi: species name (if type is species)
        classj: class name (if type is class)
    """
    # simul names
    sim_names = sorted_dfs_dct.keys()
    species_lists = np.concatenate([np.array(sorted_dfs_dct[sim_name].index) for sim_name in sim_names])
    classes_list = np.concatenate([np.array(sorted_dfs_dct[sim_name].columns) for sim_name in sim_names])
    # list of all species and classes
    all_sp = np.array(list(set(species_lists)))
    all_cl = np.sort(np.array(list(set(classes_list))))
    
    # scan all dataframes and add 0 values where sp/cl not found
    for _, df_sim in sorted_dfs_dct.items():
        for cl in all_cl:
            if cl not in df_sim.columns:
                df_sim[cl] = 0.
        for sp in all_sp:
            if sp not in df_sim.index:
                df_sim.loc[sp] = 0.
        # unneeded ; automatically rewritten # sorted_dfs_dct[sim_name] = df_sim
                
    # dataframe of FDIs
    df_FDI = pd.DataFrame(0, index=sim_names, columns=sim_names, dtype=np.float64)
    
    # calculate the differences in the omega: (om_ijn-om_ijm)^2
    for nn, n in enumerate(df_FDI.index):
        for mm, m in enumerate(df_FDI.columns):
            if mm > nn: # only low triangular, no diagonal #DOMANDA PER AN DOVREI METTERE ANCHE M=N NON RICORDO
                sim_m = sorted_dfs_dct[m]
                sim_n = sorted_dfs_dct[n]
                
                df_diff_square = (sim_n-sim_m)**2 # operations by indices
                # print(sim_n, df_diff_square)
                # now calculate FDI based on type
                if fditype == 'global':
                    df_FDI[m][n] = np.power(np.sum(df_diff_square.values), 0.5)
                elif fditype == 'species':
                    df_FDI[m][n] = np.power(np.sum(df_diff_square.loc['flux_' + speciesi]), 0.5) # sum_j: all classes for one species
                elif fditype == 'class':
                    df_FDI[m][n] = np.power(np.sum(df_diff_square[classj]), 0.5) # sum_i: all species for one class
                # print(df_FDI[m][n])
    # print(df_FDI)
    # compute mu = 1/N sum(n,m) (FDI), n != m
    mu = np.sum(df_FDI.values)/len(sim_names)
    # print(mu, len(sim_names))
    # final FDI scaled by mu
    for nn, n in enumerate(df_FDI.index):
        for mm, m in enumerate(df_FDI.columns):
            if mm > nn: # only low triangular, no diagonal 
                df_FDI[m][n] -= mu
    # print(df_FDI)
    df_FDI.sort_index(axis=0, ascending=False, inplace=True)
    df_FDI.sort_index(axis=1, inplace=True)

    return df_FDI