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
		self.flux_sorted = reaction_fluxes(rxns_sorted.rxn_class_df, verbose)
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
    
		if isinstance(tot_rop_df, pd.DataFrame):
			# concatenate
			tot_rop_df = pd.concat([tot_rop_df, tot_rop_df0])
			tot_rop_df = tot_rop_df.groupby(level=0).sum() # sum rxns with same indexes
		else:
			tot_rop_df = copy.deepcopy(tot_rop_df0)			
     		# assign flux
			# self.flux_sorted.assign_flux(tot_rop_df)
				
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
			x_axis, reaction_rate_ = GetReactionRatesIndex(kinetic_folder=self.kinetic_mechanism, 
				output_folder=results_folder, 
				reaction_index=[indici[i]-1], 
				abscissae_name=x_axis_name)
			
			nome = self.kinetic_map.ReactionNameFromIndex(indici[i]-1) # nome della reazione

			# to manage equilibrium reaction where 'species' can be on the right or on the left of '=' 
			# i.e., consistently if they are produced or consumed in a specific simulation
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