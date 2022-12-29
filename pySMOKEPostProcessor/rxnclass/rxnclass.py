'''
SCRIPT: rxnclasses
@Authors:
    Luna Pratali Maffei [1]
    [1]: CRECK Modeling Lab, Department of Chemistry, Materials, and Chemical Engineering, Politecnico di Milano
@Contacts:
    luna.pratali@polimi.it
@Additional notes:
    This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
    Please report any bug to: luna.pratali@polimi.it
'''

# Import main libraries
import pandas as pd
import sys
import os
import numpy as np
import copy

R = ['R', 'H', 'OH', 'O2', 'O', 'CH3', 'HO2', 'HCO', 'C2H3']
RSR = ['C5H5', 'C7H7', 'C6H5O']


def check_bimol_type(speciestype, reactiontype):
    """
    check if rxn is M+M, RSR+M, R+M, R+R, RSR+RSR
    """
    try:
        species_type_1 = speciestype.split('-')[-1]
    except AttributeError:
        return 'UNSORTED'
    if reactiontype == 'ENLARGE':
        return 'UNIMOL'
    # CHECK SPECIES TYPE 2
    if reactiontype.split('_')[0] in ['HABS', 'ADD', 'REC', 'ENLARGE'] and '-' not in reactiontype:
        if len(reactiontype.split('_')) == 1:
            return 'UNSORTED'
        if reactiontype.split('_')[1] in R:
            species_type_2 = 'R'
        elif reactiontype.split('_')[1] in RSR:
            species_type_2 = 'RSR'
        else:
            species_type_2 = 'NA'
    elif reactiontype.split('_')[0] in ['ADD', 'REC', 'ENLARGE'] and '-' in reactiontype:
        species_type_2 = reactiontype.split('-')[-1]
    else:
        return 'UNIMOL'

    type_list = [species_type_1, species_type_2]
    type_list.sort()

    return '+'.join(type_list)


class rxnclass:

    def __init__(self, reactions, verbose: bool):
        """ allocate dataframe 
        """

        # turn reactions into a dataframe
        # index = rxn index, columns = [classtype, class, reactiontype, flux]
        self.rxn_class_df = pd.DataFrame(index=np.arange(1, len(
            reactions)+1), columns=['name', 'classtype', 'speciestype', 'reactiontype', 'bimoltype'], dtype=object)
        self.reactions = reactions
        self.verbose = verbose
        """ assign class and sublcass
        """
        for rxn in self.reactions:
            idx = rxn['index']
            self.rxn_class_df['name'][idx] = rxn['name']
            self.rxn_class_df['speciestype'][idx] = rxn['class']
            self.rxn_class_df['reactiontype'][idx] = rxn['reactiontype']
            self.rxn_class_df['bimoltype'][idx] = check_bimol_type(
                rxn['class'], rxn['reactiontype'])

        self.rxn_class_df = self.rxn_class_df.replace('None', np.nan)
        self.rxn_class_df['speciestype'] = self.rxn_class_df['speciestype'].replace(
            np.nan, 'UNSORTED')
        self.rxn_class_df['reactiontype'] = self.rxn_class_df['reactiontype'].replace(
            np.nan, 'UNSORTED')

    def assign_class_grp(self, subcl_grp_dct):
        """ assign class group if available
        """
        for subcl, subset in self.rxn_class_df.groupby('reactiontype'):
            # None values are automatically discarded
            rxns = subset.index
            try:
                self.rxn_class_df['classtype'][rxns] = subcl_grp_dct[subcl]
            except KeyError:
                self.rxn_class_df['classtype'][rxns] = 'UNSORTED'
                print(
                    '*Warning: reactiontype {} not found in class groups'.format(subcl))
                continue

class rxnflux:
    def __init__(self, rxn_class_df, verbose: bool):
        """ initialize rxn class dataframe"""
        self.rxn_class_df = rxn_class_df
        self.verbose = verbose
        
    def assign_flux(self, tot_rop_df):
        """ assign flux from the flux analysis
        """
        # print(self.rxn_class_df.loc[tot_rop_df.index])
        self.rxn_class_df = pd.concat([self.rxn_class_df, tot_rop_df], axis=1)
        # self.rxn_class_df.join(tot_rop_df)
        # replace missing flux values with 0
        flux_sp_name = tot_rop_df.columns[0]
        self.rxn_class_df[flux_sp_name] = self.rxn_class_df[flux_sp_name].replace(
            np.nan, 0.0)

        # renormalize
        #renorm_factor = sum(abs(self.rxn_class_df[flux_sp_name]))
        
        # renormalize
        # rxn_class_df = rxn_class_df.sort_values(by='absflux', ascending = False)

    def sum_fwbw(self):
        """
        sum flux for fw and bw rxns
        if '2INDENYL=>C18H14' in self.rxn_class_df['name'].values and 'C18H14=>2INDENYL' in self.rxn_class_df['name'].values:
            idx0 = self.rxn_class_df.index[self.rxn_class_df['name'] == '2INDENYL=>C18H14'][0]
            idx1 = self.rxn_class_df.index[self.rxn_class_df['name'] == 'C18H14=>2INDENYL'][0]
            self.rxn_class_df.loc[idx0, flux_sp_name] += self.rxn_class_df.loc[idx1, flux_sp_name]
            self.rxn_class_df.loc[idx1, flux_sp_name] *= 0
            # self.rxn_class_df = self.rxn_class_df.drop(idx1, axis = 0)
        """ 
        #######################
        self.flux_cols = [
            col for col in self.rxn_class_df.columns if 'flux' in col]
        # delete row if flux is 0, much faster :)
        rows_todel = [idx for idx in self.rxn_class_df.index if all(self.rxn_class_df.loc[idx][self.flux_cols] == 0)]
        self.rxn_class_df = self.rxn_class_df.drop(rows_todel)
        #list of irrev rxns
        rxns_irrev = [rxn for rxn in self.rxn_class_df['name'] if '=>' in rxn]
        idxs_rxns_irrev = list(set([self.rxn_class_df.index[self.rxn_class_df['name'] == rxn][0] for rxn in rxns_irrev]))
        rxns_irrev_series = pd.DataFrame(index=idxs_rxns_irrev, columns=['name', 'rcts', 'prds'])
        for idx in idxs_rxns_irrev:
            rxn = self.rxn_class_df['name'][idx]
            rxns_irrev_series['name'][idx] = rxn
            rxns_irrev_series['rcts'][idx]  = '+'.join(sorted(rxn.split('=>')[0].split('+')))
            rxns_irrev_series['prds'][idx]  = '+'.join(sorted(rxn.split('=>')[1].split('+')))

        for idx0 in idxs_rxns_irrev:
            # continue if idx was removed
            if idx0 not in rxns_irrev_series.index:
                continue
            rcts, prds = rxns_irrev_series[['rcts', 'prds']].loc[idx0]
            idx1s = list(set(rxns_irrev_series.index[rxns_irrev_series['rcts'] == prds]) & set(rxns_irrev_series.index[rxns_irrev_series['prds'] == rcts]))
            for idx1 in idx1s:
                if self.rxn_class_df['speciestype'][idx1] == 'UNSORTED':
                    idxkeep = copy.deepcopy(idx0)
                    idxrem = copy.deepcopy(idx1)
                elif self.rxn_class_df['speciestype'][idx0] == 'UNSORTED':
                    idxkeep = copy.deepcopy(idx1)
                    idxrem = copy.deepcopy(idx0)
                else:
                    # pick the highest flux
                    fl0 = max(abs(self.rxn_class_df.loc[idx0, self.flux_cols]))
                    fl1 = max(abs(self.rxn_class_df.loc[idx1, self.flux_cols]))
                    maxfl = max([fl0, fl1])
                    idxkeep = [idx0, idx1][[fl0, fl1].index(maxfl)]
                    idxrem = [idx0, idx1][1-[idx0, idx1].index(idxkeep)]
                if self.verbose:
                    print('merging flux {} and removing {}'.format(self.rxn_class_df['name'][idxkeep], self.rxn_class_df['name'][idxrem]))
                self.rxn_class_df.loc[idxkeep, self.flux_cols] += self.rxn_class_df.loc[idxrem, self.flux_cols]
                self.rxn_class_df = self.rxn_class_df.drop(idxrem, axis = 0)
                rxns_irrev_series = rxns_irrev_series.drop(idxrem, axis = 0)
                      
        self.rxn_class_df_all = copy.deepcopy(self.rxn_class_df)

    def filter_class(self, filter_dct):
        """ only keep classes according to criteria listed in filter_dct
        """
        dict_indexes = dict.fromkeys(filter_dct.keys())
        for criterion, values in filter_dct.items():
            dict_indexes[criterion] = list(self.rxn_class_df[[any(v in val for v in values) for val in self.rxn_class_df[criterion]]].index)

        indexes_filter = list(set.intersection(*[set(val) for val in dict_indexes.values()]))
        self.rxn_class_df = self.rxn_class_df.loc[list(set(indexes_filter))]

    def filter_flux(self, threshold=1e-3):
        """ delete all reactions with contributions below a threshold 
        """

        indexes_filter = []

        for flux_sp_name in self.flux_cols:
            indexes_filter.extend(
                list(self.rxn_class_df[abs(self.rxn_class_df[flux_sp_name])/max(abs(self.rxn_class_df[flux_sp_name])) > threshold].index))

        self.rxn_class_df = self.rxn_class_df.loc[list(set(indexes_filter))]

    def sortby(self, sortlist):
        """ sum fluxes by criteria in sortlist
        """
        # check that all criteria are columns
        if not all(criterion in self.rxn_class_df.columns for criterion in sortlist):
            print('*Error: criteria not all present in dataframe columns - exiting')
            sys.exit()

        # group and sum
        new_sort_df = pd.DataFrame(index=self.flux_cols)
        if len(sortlist) == 1:
            sortlist = sortlist[0] # avoid pandas warning for single grouper
            
        for grp_idx, grp_df in self.rxn_class_df.groupby(sortlist):
            if isinstance(grp_idx, str):
                name = grp_idx
            else:
                name = '['+']['.join(grp_idx)+']'
            if self.verbose:
                print(grp_idx, '\n', grp_df, '\n')
            new_sort_df[name] = grp_df[self.flux_cols].sum()

        # renormalize by species
        
        for flux_sp_name in new_sort_df.index:
            renorm_factor = max(abs(new_sort_df.loc[flux_sp_name]))
            weight_factor = sum(abs(self.rxn_class_df[flux_sp_name]))/sum(abs(self.rxn_class_df_all[flux_sp_name]))
            #new_sort_df.loc[flux_sp_name] /= renorm_factor
            new_sort_df.loc[flux_sp_name] *= (weight_factor/renorm_factor)

        if self.verbose:
            print(new_sort_df)

        return new_sort_df


