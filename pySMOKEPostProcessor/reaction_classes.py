import pandas as pd
import numpy as np
import copy
from operator import add, neg

from .ropa import RateOfProductionAnalysis, GetReactionRatesIndex
from .maps.KineticMap import KineticMap
from .reaction_classes_utilities.reaction_classes_groups import ReadReactionsGroups
from .reaction_classes_utilities.reaction_classes import reaction_classes
from .reaction_classes_utilities.reaction_classes import reaction_fluxes


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
		_, subcl_grp_dct = ReadReactionsGroups(
		    classes_definition)

        # sort
		rxns_sorted = reaction_classes(reactions_all, verbose=False)
		rxns_sorted.assign_class_grp(subcl_grp_dct)

		# assign to self
		self.rxns_sorted = rxns_sorted
		self.flux_sorted = reaction_fluxes(rxns_sorted.rxn_class_df, verbose) #needed for cumulative reaction rates - but should be removed
		self.kinetic_mechanism = kinetic_mechanism
		self.classes_definition = classes_definition
		self.verbose = verbose
		self.kinetic_map = kinetics
		self.reactions_all = reactions_all

	def process_flux(self,
				species_list,
				results_folder,
				n_of_rxns=100,
				ropa_type='global',
				mass_ropa = False):

		# reinitialize
		self.flux_sorted = reaction_fluxes(self.rxns_sorted.rxn_class_df, self.verbose)
  
		if self.verbose:
			print('processing simul {}'.format(results_folder))

		# distinguish pp input based on ropa type
		loc_low_up = np.array([0, 0, 0, ], dtype=float)
		if isinstance(ropa_type, dict):
			if 'local' in ropa_type.keys():
				loc_low_up[0] = ropa_type['local']
				ropa_type = 'local'
			elif 'region' in ropa_type.keys():
				loc_low_up[1:] = ropa_type['region']
				ropa_type = 'region'

        # simul output
		for sp in species_list:

			if isinstance(sp, str):
				sps = [sp]
				spname = sp
			elif isinstance(sp, dict):
				spname = list(sp.keys())[0]
				sps = sp[spname]
				if isinstance(sps, list) == False:
					raise TypeError('in spc dictionary, the value must be a list of species')
			else:
				raise TypeError('species must be a single string or a dictionary with a list of species')
    
			tot_rop_df = None
			for sp in sps:
				indice = self.kinetic_map.IndexFromSpeciesName(sp)
				mwi = self.kinetic_map.mws[indice]

				tot_rop, indexes, _ = RateOfProductionAnalysis(kinetic_folder=self.kinetic_mechanism, 
															output_folder=results_folder, 
															species = sp, 
															ropa_type = ropa_type, 
															local_value = loc_low_up[0],
															lower_value = loc_low_up[1], 
															upper_value = loc_low_up[2], 
															number_of_reactions = n_of_rxns)
				
				if mass_ropa==True:
					tot_rop = [i * mwi for i in tot_rop]

				tot_rop_df0 = pd.DataFrame(tot_rop, index=np.array(indexes)+1, columns=['flux_{}'.format(spname)], dtype=float)
				tot_rop_df0 = tot_rop_df0.groupby(level=0).sum() # sum rxns with same indexes
    
				if isinstance(tot_rop_df, pd.DataFrame):
					# concatenate
					tot_rop_df = pd.concat([tot_rop_df, tot_rop_df0])
					tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
				else:
					tot_rop_df = copy.deepcopy(tot_rop_df0)			

				# check and ask luna why first row of tot_rop_df contains the first reaction 
				# of the kinetic model even if it does not include the selected species

     		# assign flux
			self.flux_sorted.assign_flux(tot_rop_df)

		self.flux_sorted.sum_fwbw()

	def sort_and_filter(self, sortlist, filter_dct = {}, thresh = 1e-3, weigheach = True):
		# filter rxns
		rxns_sorted = copy.deepcopy(self.flux_sorted)
		if len(filter_dct) > 0:
			rxns_sorted.filter_class(filter_dct)
		# filter flux
		rxns_sorted.filter_flux(threshold=thresh)
		# sum same speciestype-classgroup-reactiontype together
		sortdf = rxns_sorted.sortby(sortlist, weigheach = weigheach)
		# drop unsorted cols
		col_names = sortdf.columns
		for col in col_names:
			if 'UNSORTED' in col:
				sortdf = sortdf.drop(col, axis=1)

		return sortdf

	# new function to compute and plot reaction class rate profiles along axial coordinate
	def process_reaction_class_rate(self, results_folder: str, x_axis_name: str, reactionclass_type: str):
    # to be extended to all types (reactiontype, classtype, speciestype, bimoltype. requires a call to sort_and_filter first)
	# do it similar to sort_and_filter, with sortlist (which only provides criteria for getting the rates) and filter_dct
		indici = [i['index']-1 for i in self.reactions_all if not i['reactiontype'] == None if reactionclass_type in i['reactiontype']]

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
										rate_type = 'TOT',
										filter_ClassesToPlot = [],
										threshold = 5e-2,
          								n_of_rxns = 20,
          								verbose = False):

		# ROPA ONLY NEEDED FOR RXN INDEXES - BASED ON GLOBAL ROPA
		tot_rop, indexes, _ = RateOfProductionAnalysis(kinetic_folder=self.kinetic_mechanism, 
														output_folder=results_folder, 
														species = species, 
														ropa_type = 'global', 
														number_of_reactions = n_of_rxns)
		col_species = 'flux_' + species
		tot_rop_df0 = pd.DataFrame(tot_rop, index=np.array(indexes)+1, columns=[col_species], dtype=float)
		tot_rop_df0 = tot_rop_df0.groupby(level=0).sum() # sum rxns with same indexes
		tot_rop_df = copy.deepcopy(tot_rop_df0)	
				
		#to be fixed - it will be called for rxn class grouping # self.flux_sorted.sum_fwbw() # some errors to be fixed. Ask Luna

		# sort by absolute flux
		tot_rop_df['absflux'] = abs(tot_rop_df[col_species].values)
		# indexes for production and consumption
		newPCcol = list([tot_rop_df[col_species] >= 0][0])
		newPCcol = ['P'*(i==True) + 'C'*(i==False) for i in newPCcol]
		tot_rop_df['PC'] =  newPCcol
		# sort by max abs flux
		tot_rop_df = tot_rop_df.sort_values(by = 'absflux', ascending = False)

		reaction_rate_all = []
		matrix_of_rates_all = []
		matrix_of_rates = []
		rate_percentage_contribution = []
		nomi = []

		if verbose: print(tot_rop_df)
          
		for index in tot_rop_df.index:
			rxn_type = tot_rop_df['PC'][index]
   
			x_axis, reaction_rate_ = GetReactionRatesIndex(kinetic_folder = self.kinetic_mechanism, 
				output_folder=results_folder, 
				reaction_index=[index - 1], 
				abscissae_name=x_axis_name)
			
			name = self.kinetic_map.ReactionNameFromIndex(index - 1) # name della reazione

			# put production rates positive and consumption rates negative
			rcts = name.split(':')[-1].split('=')[0].strip().split('(+M)')[0].split('+')
			prds = name.split(':')[-1].split('=')[-1].strip().split('(+M)')[0].split('+')
   
			if verbose : print('rxn: {}, rcts: {}; prds: {}'.format(index, rcts, prds))
   
			if rxn_type == 'P' and species in rcts: # if species is produced from a reversible reactions the rate will appear negative but it shouldn't
				reaction_rate_ = list( map(neg, reaction_rate_))
			elif rxn_type == 'C' and species in rcts: # when species is consumed and it is in the reactants; put flux to negative
				reaction_rate_ = list( map(neg, reaction_rate_))
			# elif rxn_type == 'C' and species in prds: do not change sign, it will already be negative

			# IN FUTURE_ MOVE THIS SECTION AS AN ADDITIONAL ONE AFTER ASSIGNING ALL RATES - 
   			# to plot reactions only in specific reaction class; ADDITIONAL OPTION: PLOT RXNS BY CLASS
			ToPlot = 1
			if len(filter_ClassesToPlot) >= 1:
				ToPlot = 0
				for j in range(len(filter_ClassesToPlot)):
					indici_ToPlot = [k['index']-1 for k in self.reactions_all if not k['reactiontype'] == None if filter_ClassesToPlot[j] in k['reactiontype']]
					if index in indici_ToPlot:
						ToPlot = ToPlot + 1
				
				if ToPlot == 0:
					reaction_rate_ = [0] * len(reaction_rate_)

			if ToPlot == 1 and rxn_type == rate_type or rate_type == 'TOT': # add for plotting only allowed rate type
				nomi.append(self.kinetic_map.ReactionNameFromIndex(index-1)[:30])
				matrix_of_rates_all.append(reaction_rate_)
				# print(self.kinetic_map.ReactionNameFromIndex(index-1)[:30])
				if len(nomi) == 1:
					reaction_rate_all = map(abs, reaction_rate_)
				else:
					reaction_rate_all = list( map(add, reaction_rate_all, list( map(abs, reaction_rate_)))) # sum absolute values
				
		nomi_ret = []
		total_rate_area = np.trapz(y = reaction_rate_all, x = x_axis)
		for i, _ in enumerate(nomi):
			single_rate_area = np.trapz(y = list(map(abs, matrix_of_rates_all[i])), x = x_axis) # compare absolute values to set the threshold
			rate_percentage_contribution.append(single_rate_area / total_rate_area * 100)	
			if rate_percentage_contribution[-1]/100 > threshold:
				nomi_ret.append(nomi[i] + ' ' + str(round(rate_percentage_contribution[-1],1))+ ' %')
				matrix_of_rates.append(matrix_of_rates_all[:][i])
			else:
				rate_percentage_contribution.pop(-1)
	
		if verbose == True:
			print("rate percentage contribution: \n", rate_percentage_contribution)
		
		return x_axis, matrix_of_rates, nomi_ret

def merge_maps_onespecies(sorted_dfs_dct):
	""" combines the heatmaps of different simulations for the same set of species and puts them in a new dataframe
	Args:
		sorted_dfs ({idx: dataframe}): sorted dataframes with fluxes.
	"""
 
	# simul names
	sim_names = sorted_dfs_dct.keys()
	species_lists = np.concatenate([np.array(sorted_dfs_dct[sim_name].index) for sim_name in sim_names])
	classes_list = np.concatenate([np.array(sorted_dfs_dct[sim_name].columns) for sim_name in sim_names])
  	# find common species and classes
	common_sp = np.array(list(set(species_lists)))
	common_cl = np.sort(np.array(list(set(classes_list))))
 	# for each species: rename according to simulation name and concatenate dataframes
	dftot = pd.DataFrame(columns = common_cl)

	for sim_name, dffull in sorted_dfs_dct.items():
		# filter indexes
		pdnew = dffull.loc[common_sp]
		# rename indexes according to simul name
		pdnew = pdnew.rename(index = lambda spname: spname + '-' + str(sim_name))
		# now concate to dftot
		dftot = pd.concat([dftot, pdnew])
  
	# replace nan with 0
	dftot = dftot.replace(np.nan, 0)
	# order according to index, so you have all species in rows
	dftot = dftot.sort_index()
 
	return dftot
			
			
 
 
	
 
