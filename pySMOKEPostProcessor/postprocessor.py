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
                                 number_of_reactions: int = 10) -> dict:
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
        sensitivity_coefficients = widget.coefficients()

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
                         reaction_index: list = None):

        if reaction_name is not None:
            reaction_index = self.km.ReactionIndexFromName(name=reaction_name)

        widget = ROPA()
        widget.setDatabase(self.db)
        # TODO Refactor the cpp function getReactionRates
        # widget.getReactionRates(reaction_index)
        # return None

    def GetFormationRates(self, formation_rate_type: str,
                          species_names: list = None,
                          species_index: list = None):

        allowed_types = ['net', 'production', 'destruction', 'characteristic-time']
        if formation_rate_type not in allowed_types:
            raise ValueError('Available types for the formation rate are: net | production | destruction | characteristic-time')

        widget = ROPA()
        widget.setDatabase(self.db)
        # TODO Refactor the cpp function getFormationRates
        # widget.getReactionRates(reaction_index)
        # return None

    def SensitivityCoefficients(self, target: str, reaction_name: str,
                                normalization_type: str):

        if (normalization_type != 'local' and normalization_type != 'max-value'):
            raise ValueError('Please select one of the available normalization: local | max-value')

        # TODO refactor of the function
