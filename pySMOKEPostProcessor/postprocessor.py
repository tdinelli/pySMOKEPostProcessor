from pySMOKEPostProcessor import ProfilesDatabase, ROPA, Sensitivity
from maps.KineticMap import KineticMap
from graph_writer import GraphWriter


class PostProcessor:
    def __init__(self, kineticFolder: str, outputFolder: str) -> None:

        self.db = ProfilesDatabase()
        self.db.readFileResults(outputFolder)
        self.db.readKineticMechanism(kineticFolder)

        self.kineticFolder = kineticFolder
        self.outputFolder = outputFolder

        self.km = KineticMap(self.kineticFolder)

    def RateOfProductionAnalysis(self,
                                 species: str,
                                 ropa_type: str,
                                 local_value: float = 0,
                                 lower_value: float = 0,
                                 upper_value: float = 0,
                                 number_of_reactions: int = 10,
                                 two_dimensions: bool = False,
                                 region_location: dict = None) -> dict:
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

            ropa_result = {'coefficients': ropa_coefficients,
                           'reaction_names': reaction_names,
                           'reaction_indices': reaction_indices}

            return ropa_result
        else:
            return self.RateOfProductionAnalysis2D(species, ropa_type,
                                                   number_of_reactions,
                                                   region_location)

    def RateOfProductionAnalysis2D(self, species: str, ropa_type: str,
                                   number_of_reactions: int = 10,
                                   region_location: dict = None) -> dict:
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
            secondNames.append(self.km.SpeciesNameFromIndex(indexSecondName[i]))

        Graph = GraphWriter(flux_analysis_type, species, element)
        Graph = Graph.CreateGraph(firstNames, secondNames, computedThickness, computedLabel)

        return Graph

    def GetReactionRates(self, reaction_name: list = None,
                         reaction_index: list = None,
                         sum_rates: bool = False):
        if reaction_name is not None:
            reaction_index = [self.km.ReactionIndexFromName(name=i) for i in reaction_name]
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
        widget.getSensitivityProfiles(reaction_index)
        sensitivity_coefficients = widget.sensitivityCoefficients()

        return sensitivity_coefficients
