from .pySMOKEPostProcessor import ProfilesDatabase, ROPA, Sensitivity
from .maps.KineticMap import KineticMap
from .graph_writer import GraphWriter


class PostProcessor:
    def __init__(self, kineticFolder: str, outputFolder: str) -> None:

        self.db = ProfilesDatabase()
        self.db.readFileResults(outputFolder)
        self.db.readKineticMechanism(kineticFolder)

        self.kineticFolder = kineticFolder
        self.outputFolder = outputFolder

        self.km = KineticMap(self.kineticFolder)

    def convert_tomass(self,
                       ropa_coefficients: list,
                       species: str):
        # species index
        sp_idx = self.km.IndexFromSpeciesName(species)
        # molecular weight
        mwi = self.km.mws[sp_idx]
        # derive mass based ropa
        ropa_coefficients = [c*mwi for c in ropa_coefficients]
        return ropa_coefficients

    def RateOfProductionAnalysis(self,
                                 species: str,
                                 ropa_type: str,
                                 local_value: float = 0,
                                 lower_value: float = 0,
                                 upper_value: float = 0,
                                 number_of_reactions: int = 10,
                                 two_dimensions: bool = False,
                                 region_location: dict = None,
                                 mass_ropa: bool = False) -> dict:
        if (two_dimensions is False):
            widget = ROPA()
            widget.setDataBase(self.db)
            widget.setROPAType(ropa_type)
            widget.setSpecies(species)
            widget.setLocalValue(local_value)
            widget.setLowerBound(lower_value)
            widget.setUpperBound(upper_value)

            widget.rateOfProductionAnalysis(number_of_reactions)

            reaction_indices = widget.reactions()
            ropa_coefficients = widget.coefficients()

            reaction_names = []
            for i in reaction_indices:
                reaction_names.append(self.km.ReactionNameFromIndex(i))

            if mass_ropa:
                ropa_coefficients = self.convert_tomass(ropa_coefficients,
                                                        species)

            ropa_result = {'coefficients': ropa_coefficients,
                           'reaction_names': reaction_names,
                           'reaction_indices': reaction_indices}

            return ropa_result
        else:
            return self.RateOfProductionAnalysis2D(species, ropa_type,
                                                   number_of_reactions,
                                                   region_location,
                                                   mass_ropa)

    def RateOfProductionAnalysis2D(self, species: str, ropa_type: str,
                                   number_of_reactions: int = 10,
                                   region_location: dict = None,
                                   mass_ropa: bool = False) -> dict:
        widget = ROPA()
        widget.setDataBase(self.db)
        widget.setROPAType(ropa_type)
        widget.setSpecies(species)
        widget.setLocalValue(0)
        widget.setLowerBound(0)
        widget.setUpperBound(0)

        local_value_x = region_location['local_value_x']
        local_value_z = region_location['local_value_z']
        lower_value_x = region_location['lower_value_x']
        lower_value_z = region_location['lower_value_z']
        upper_value_x = region_location['upper_value_x']
        upper_value_z = region_location['upper_value_z']

        widget.RateOfProductionAnalysis2D(number_of_reactions, local_value_x,
                                          local_value_z, lower_value_x,
                                          upper_value_x, lower_value_z,
                                          upper_value_z)

        reaction_indices = widget.reactions()
        ropa_coefficients = widget.coefficients()

        reaction_names = []
        for i in reaction_indices:
            reaction_names.append(self.km.ReactionNameFromIndex(i))

        if mass_ropa:
            ropa_coefficients = self.convert_tomass(ropa_coefficients,
                                                    species)

        ropa_result = {'coefficients': ropa_coefficients,
                       'reaction_names': reaction_names,
                       'reaction_indices': reaction_indices}

        return ropa_result

    def SensitivityAnalysis(self, target: str, sensitivity_type: str,
                            ordering_type: str, normalization_type: str,
                            local_value: float = 0, lower_value: float = 0,
                            upper_value: float = 0,
                            number_of_reactions: int = 10) -> dict:

        # SENSITIVITY HERE
        widget = Sensitivity()

        widget.setDataBase(self.db)
        widget.setSensitivityType(sensitivity_type)
        widget.setOrderingType(ordering_type)
        widget.setNormalizationType(normalization_type)
        widget.setTarget(target)
        widget.setLocalValue(local_value)
        widget.setLowerBound(lower_value)
        widget.setUpperBound(upper_value)
        widget.prepare()
        widget.readSensitivityCoefficients()
        widget.sensitivityAnalysis(number_of_reactions)

        reaction_indices = widget.reactions()
        sensitivity_coefficients = widget.sensitivityCoefficients()

        reaction_names = []
        for i in reaction_indices:
            reaction_names.append(self.km.ReactionNameFromIndex(i))

        sensitivity_result = {'coefficients': sensitivity_coefficients,
                              'reaction_names': reaction_names,
                              'reaction_indices': reaction_indices}

        return sensitivity_result

    def FluxAnalysis(self, species: str, element: str, flux_analysis_type: str,
                     thickness: str, thickness_log_scale: bool,
                     label_type: str, depth: int = 2, width: int = 5,
                     threshold: float = 0, local_value: float = 0.01):

        widget = ROPA()

        widget.setDataBase(self.db)
        widget.setSpecies(species)
        widget.setElement(element)
        widget.setFluxAnalysisType(flux_analysis_type)
        widget.setLocalValue(local_value)
        widget.setThickness(thickness)
        widget.setThicknessLogScale(thickness_log_scale)
        widget.setLabelType(label_type)
        widget.setDepth(depth)
        widget.setWidth(width)
        widget.setThreshold(threshold)

        widget.fluxAnalysis()

        indexFirstName = widget.indexFirstName()
        indexSecondName = widget.indexSecondName()
        computedThickness = widget.computedThickness()
        computedLabel = widget.computedLabel()

        firstNames = []
        secondNames = []
        for i, j in enumerate(indexFirstName):
            firstNames.append(self.km.SpeciesNameFromIndex(j))
            secondNames.append(
                self.km.SpeciesNameFromIndex(indexSecondName[i]))
        Graph = GraphWriter(flux_analysis_type)  # , species, element)
        Graph = Graph.CreateGraph(
            firstNames, secondNames, computedThickness, computedLabel)

        return Graph

    def GetReactionRates(self, reaction_name: list = None,
                         reaction_index: list = None,
                         sum_rates: bool = False):
        if reaction_name is not None:
            reaction_index = [self.km.ReactionIndexFromName(
                name=i) for i in reaction_name]
        widget = ROPA()
        widget.setDataBase(self.db)
        widget.getReactionRates(reaction_index, sum_rates)

        if (sum_rates):
            reaction_rates = widget.sumOfRates()
        else:
            reaction_rates = widget.reactionRates()

        return reaction_rates

    def GetFormationRates(self, formation_rate_type: str,
                          species: str,
                          units: str = "mole"):
        widget = ROPA()
        widget.setDataBase(self.db)
        widget.getFormationRates(species, units, formation_rate_type)
        formationRates = widget.formationRates()

        return formationRates

    def SensitivityCoefficients(self,
                                target: str,
                                normalization_type: str,
                                reaction_name: str = None,
                                reaction_index: int = None):

        if reaction_name is not None:
            reaction_index = self.km.ReactionIndexFromName(name=reaction_name)

        widget = Sensitivity()
        widget.setDataBase(self.db)
        widget.setSensitivityType("global")
        widget.setOrderingType("peak-values")
        widget.setNormalizationType(normalization_type)
        widget.setTarget(target)
        widget.setLocalValue(0.)
        widget.setLowerBound(0.)
        widget.setUpperBound(0.)
        widget.prepare()
        widget.readSensitivityCoefficients()
        widget.getSensitivityProfile(reaction_index)
        sensitivity_coefficients = widget.sensitivityCoefficients()

        return sensitivity_coefficients


    # new function to compute plot cumulative contribution of different reactions
    # to production/consumption rate profile of a species
    # DA RISCRIVERE COMPLETAMENTE, TUTTE LE FUNZIONI SONO CAMBIATE

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
