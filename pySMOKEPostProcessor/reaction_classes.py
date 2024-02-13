import copy
import numpy as np
import pandas as pd

from .reaction_classes_utilities.reaction_classes_groups import ReadReactionsGroups
from .reaction_classes_utilities.reaction_classes_calc import reaction_classes_assign
from .reaction_classes_utilities.reaction_classes_calc import reaction_fluxes


def assignclass(kinmap, classes_definition):
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
    rxns_sorted = reaction_classes_assign(reactions_all, verbose=False)
    rxns_sorted.assign_class_grp(subcl_grp_dct)

    return rxns_sorted, reactions_all


class FluxByClass:

    def __init__(self, rxns_sorted, reactions_all=[], verbose: bool = False):

        # assign to self
        self.rxns_sorted = rxns_sorted
        # was put for cumulative rxn rates
        # self.flux_sorted = reaction_fluxes(rxns_sorted.rxn_class_df, verbose)
        # needed for cumulative reaction rates - but should be removed
        self.verbose = verbose
        self.reactions_all = reactions_all

    def process_flux(self, species_list, tot_rop_dct):
        # input tot_rop_dct: dictionary with ROPA performed for a set of
        # species {spc: {ropa dct}}
        # reinitialize
        self.flux_sorted = reaction_fluxes(
            self.rxns_sorted.rxn_class_df, self.verbose)

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
                                           columns=['flux_{}'.format(spname)], dtype=np.float32)
                #  quello sotto dovrebbe essere sufficiente
                # tot_rop_df0 = tot_rop_df0.groupby(level=0).sum() # sum rxns with same indexes

                if isinstance(tot_rop_df, pd.DataFrame):
                    # concatenate
                    tot_rop_df = pd.concat([tot_rop_df, tot_rop_df0])
                    #  quello sotto dovrebbe essere sufficiente
                    # tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes

                else:
                    tot_rop_df = copy.deepcopy(tot_rop_df0)

                # Luna: nego - ho controllato e mi sembra a posto
                # check and ask luna why first row of tot_rop_df contains the first reaction
                # of the kinetic model even if it does not include the selected species

            # sum rxns with same indices
            # sum rxns with same indexes LPM aggiunto qui
            tot_rop_df = tot_rop_df.groupby(level=0).sum()
            # replace nan with 0
            tot_rop_df = tot_rop_df.replace(np.nan, 0)
            # concatenate flux to the dataframe of rxn classes
            self.flux_sorted.assign_flux(tot_rop_df)

        self.flux_sorted.netfluxes()

    def sort_and_filter(self,
                        sortlist,
                        filter_dct: dict = {},
                        thresh: float = 1e-3,
                        weigh: str = 'false',
                        dropunsorted: bool = True):
        # weight options: normbyspecies, omegaij, false
        # deepcopy if you need to do it multiple times
        # filter rxns
        rxns_sorted = copy.deepcopy(self.flux_sorted)
        if len(filter_dct) > 0:
            rxns_sorted.filter_class(filter_dct)
        # filter flux
        rxns_sorted.filter_flux(threshold=thresh)
        # sum same speciestype-classgroup-reactiontype together
        sortdf = rxns_sorted.sortby(
            sortlist, weigh=weigh, dropunsorted=dropunsorted)

        return sortdf

    # new function to compute and plot reaction class rate profiles along axial coordinate


def merge_maps_byspecies(sorted_dfs_dct, tosum: bool = False):
    """
    combines the heatmaps of different simulations for the same set of species
    and puts them in a new dataframe tosum: specifies if you have to sum the
    flux for each species or not
    Args:
        sorted_dfs ({idx: dataframe}): sorted dataframes with fluxes.
    """

    # simul names
    sim_names = sorted_dfs_dct.keys()
    species_lists = list(np.concatenate([np.array(sorted_dfs_dct[sim_name].index) for sim_name in sim_names]))
    classes_list = list(np.concatenate([np.array(sorted_dfs_dct[sim_name].columns) for sim_name in sim_names]))
    # find common species and classes
    all_sp = np.array(sorted(set(species_lists), key=species_lists.index))
    
    # for each species: rename according to simulation name and concatenate dataframes
    dftot = pd.DataFrame()
    for sim_name, dffull in sorted_dfs_dct.items():
        # filter indexes
        pdnew = dffull.loc[all_sp]
        # rename indexes according to simul name
        if tosum is False:
            pdnew = pdnew.rename(index=lambda spname: spname + '-' + str(sim_name))

        if len(dftot) == 0:
            dftot = pdnew
            continue
        if tosum is False:
            # in case of future warnings
            # if not all([col in dftot.columns for col in pdnew.columns]):
            #     colstoadd = [col for col in pdnew.columns if col not in dftot.columns]
            #     dftot[colstoadd] = 0.
                
            #elif not all([col in pdnew.columns for col in dftot.columns]):
            #    colstoadd = [col for col in dftot.columns if col not in pdnew.columns]
            #    pdnew[colstoadd] = 0.
                
            dftot = pd.concat([dftot, pdnew]) 
        elif tosum is True:
            dftot = dftot.add(pdnew, fill_value=0.)

    # replace nan with 0
    dftot = dftot.replace(np.nan, 0)
    # order according to index, so you have all species in rows
    if tosum is False:
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
        fditype : global (sum over ij), species (sum over j),
                  class (sum over i)
        speciesi: species name (if type is species)
        classj: class name (if type is class)
    """
    # simul names
    sim_names = sorted_dfs_dct.keys()
    species_lists = np.concatenate(
        [np.array(sorted_dfs_dct[sim_name].index) for sim_name in sim_names])
    classes_list = np.concatenate(
        [np.array(sorted_dfs_dct[sim_name].columns) for sim_name in sim_names])
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

    # dataframe of FDIs
    df_FDI = pd.DataFrame(0., index=sim_names, columns=sim_names, dtype=np.float64)

    # calculate the differences in the omega: (om_ijn-om_ijm)^2
    df_FDI.sort_index(axis=0, inplace=True)
    df_FDI.sort_index(axis=1, inplace=True)
    for nn, n in enumerate(df_FDI.index):
        for mm, m in enumerate(df_FDI.columns):
            if mm > nn:  # only low triangular, no diagonal #DOMANDA PER AN DOVREI METTERE ANCHE M=N NON RICORDO
                sim_m = sorted_dfs_dct[m]
                sim_n = sorted_dfs_dct[n]

                df_diff_square = (sim_n-sim_m)**2  # operations by indices
                # print(sim_n, df_diff_square)
                # now calculate FDI based on type
                if fditype == 'global':
                    df_FDI.loc[n, m] = np.power(np.sum(df_diff_square.values), 0.5)
                elif fditype == 'species':
                    # sum_j: all classes for one species
                    df_FDI.loc[n, m] = np.power(
                        np.sum(df_diff_square.loc['flux_' + speciesi]), 0.5)
                elif fditype == 'class':
                    # sum_i: all species for one class
                    df_FDI.loc[n, m] = np.power(np.sum(df_diff_square[classj]), 0.5)
                # print(df_FDI[m][n])
    # print(df_FDI)
    # compute mu = 1/N sum(n,m) (FDI), n != m
    setofnm = len(sim_names)*(len(sim_names)-1)/2
    mu = np.sum(df_FDI.values)/setofnm
    # print(mu, len(sim_names))
    # final FDI scaled by mu
    for nn, n in enumerate(df_FDI.index):
        for mm, m in enumerate(df_FDI.columns):
            if mm > nn:  # only low triangular, no diagonal
                df_FDI.loc[n, m] -= mu
    # print(df_FDI)
    df_FDI.sort_index(axis=0, ascending=False, inplace=True)
    df_FDI.sort_index(axis=1, inplace=True)

    return df_FDI
