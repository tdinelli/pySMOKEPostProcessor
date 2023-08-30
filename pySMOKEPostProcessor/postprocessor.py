from pySMOKEPostProcessor import ProfilesDatabase, ROPA, Sensitivity
from maps.KineticMap import KineticMap


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

        allowed_sensitivity_types = ['global', 'local', 'region']
        allowed_ordering_types = ['peak-values', 'area', 'absolute-area']
        allowed_normalization_types = ['local', 'max-value']

        if (sensitivity_type not in allowed_sensitivity_types):
            raise ValueError('Please select one of the available Sensitivity analysis type global | local | region')

        if (ordering_type not in allowed_ordering_types):
            raise ValueError('Please select one of the available ordering type: peak-values | area | absolute-area')

        if (normalization_type not in allowed_normalization_types):
            raise ValueError('Please select one of the available normalization: local | max-value')

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
