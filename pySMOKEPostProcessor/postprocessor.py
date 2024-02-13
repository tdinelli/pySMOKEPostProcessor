import pandas as pd
import numpy as np
from .pySMOKEPostProcessor import ProfilesDatabase, ROPA, Sensitivity
from .maps.KineticMap import KineticMap
from .graph_writer import GraphWriter


class PostProcessor:
    """
    Main Class of the package, needed to call the C++ backend
    Attributes:
        db: Object representing the Output.xml file inside the C++ code
        kineticFolder: Path pointing to the folder containing the kinetic mechanism.
        outputFolder: Path pointing to the folder containing the Simulations Output.
        km: Internal object representing the kinetic map. (TODO: replace in favour of OpenSMOKE_Interfaces)
    """

    def __init__(self, kineticFolder: str, outputFolder: str) -> None:

        self.db = ProfilesDatabase()
        self.db.readFileResults(outputFolder)
        self.db.readKineticMechanism(kineticFolder)

        self.kineticFolder = kineticFolder
        self.outputFolder = outputFolder

        self.km = KineticMap(self.kineticFolder)

    def RateOfProductionAnalysis(self, species: str, ropa_type: str, local_value: float = 0, lower_value: float = 0,
                                 upper_value: float = 0, number_of_reactions: int = 10, two_dimensions: bool = False,
                                 region_location: dict = None, mass_ropa: bool = False,) -> dict:
        """
        Function that performs the [R]ate [O]f [P]roduction [A]nalysis
        Args:
            species: Name of the target species for the ROPA
            ropa_type: Type of ROPA to be performed available are: gloabal | local | region
            local_value: Local value of the domain in where perform the ROPA
            lower_value: Lower value of the domain for the region ROPA
            upper_value: Upper value of the domain for the region ROPA
            number_of_reactions: Number Of Reactions to return after the ROPA
            two_dimensions: Activate the support for the ROPA for 2D/3D simulations (TODO: find a better name)
            region_location: 2D option
            mass_ropa: Return the ROPA coefficients in mass unit

        Returns:
            A dictionary as the following one:
                ropa_results = {'coefficients': [...],
                                'reaction_names': [...],
                                'reaction_indices': [...]}
                Containing the ROPA coefficients, the reaction names and the indices of the reactions.
        """

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

    def RateOfProductionAnalysis2D(self, species: str, ropa_type: str, number_of_reactions: int = 10,
                                   region_location: dict = None, mass_ropa: bool = False) -> dict:
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

    def SensitivityAnalysis(self, target: str, sensitivity_type: str, ordering_type: str, normalization_type: str,
                            local_value: float = 0, lower_value: float = 0, upper_value: float = 0,
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

    def FluxAnalysis(self, species: str, element: str, flux_analysis_type: str, thickness: str,
                     thickness_log_scale: bool, label_type: str, depth: int = 2, width: int = 5,
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

    def GetReactionRates(self, reaction_name: list = None, reaction_index: list = None, sum_rates: bool = False):
        if reaction_name is not None:
            reaction_index = [self.km.ReactionIndexFromName(
                name=i) for i in reaction_name]
        widget = ROPA()
        widget.setDataBase(self.db)
        widget.getReactionRates(reaction_index, sum_rates)

        if (sum_rates):
            reaction_rates = [widget.sumOfRates()]
        else:
            reaction_rates = widget.reactionRates()

        return reaction_rates

    def GetFormationRates(self, formation_rate_type: str, species: str, units: str = "mole"):
        widget = ROPA()
        widget.setDataBase(self.db)
        widget.getFormationRates(species, units, formation_rate_type)
        formationRates = widget.formationRates()

        return formationRates

    def SensitivityCoefficients(self, target: str, normalization_type: str,
                                reaction_name: str = None, reaction_index: int = None):

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

    def convert_tomass(self, ropa_coefficients: list, species: str) -> list:
        """
        Function that converts the rate of production coefficients from mole
        units to mass units.
        Args:
            ropa_coefficients: list containing the rate of production
            coefficients
            species: species name
        Returns:
            list containing the rate of production coefficients in mass unit.
        """
        sp_idx = self.km.IndexFromSpeciesName(species)
        mwi = self.km.mws[sp_idx]
        ropa_coefficients = [c*mwi for c in ropa_coefficients]

        return ropa_coefficients

    def reactionrategroups(self, rxnnames_sr, xaxis: list, threshold: float = 0.01):
        # reaction rates by groups (example: by class)
        # rxnnames_sr: series with labels and reaction names
        # xaxis
        # threshold: plot only if contributes above threshold% to the total rate
        rr = dict.fromkeys(rxnnames_sr.index)
        rrsum = pd.Series(index=rxnnames_sr.index, dtype=np.float64)
        for label, rxnnames in rxnnames_sr.items():
            rr[label] = np.array(self.GetReactionRates(reaction_name=rxnnames, sum_rates=True)[0])
            rrsum[label] = np.trapz(y=rr[label], x=xaxis)

        # check cumulative contribution and filter based on threshold
        rrsum /= np.sum(abs(rrsum))  # abs?
        filteredlabels = list(rrsum[abs(rrsum) > threshold].index)
        filtered_rr = [rr[key] for key in filteredlabels]
        rates_df = pd.DataFrame(np.array(filtered_rr).T, columns=filteredlabels, index=xaxis)

        return rates_df

    def cumulativerates(self, xaxis: list, ropa_dct: dict, rate_type: str = 'PC', threshold: float = 0.01):
        # cumulative reaction rate matrix extract
        # rate_type: PC, P, C (net, production, consumption)
        # threshold: delete rates based on % contribution (default: keep only those contributing > 1%)
        # xaxis: derived from output

        # 0. ropa DCT: sum coefficients for duplicates
        coefficients, indices, names = [], [], []
        allindices_array = np.array(ropa_dct['reaction_indices'])
        allcoeffs_array = np.array(ropa_dct['coefficients'])
        for i, idx in enumerate(allindices_array):
            if idx not in indices:
                indices.append(idx)
                names.append(ropa_dct['reaction_names'][i])
                if ropa_dct['reaction_indices'].count(idx) > 1:
                    positions = np.where((allindices_array == idx))[0]
                    coefficients.append(np.sum(allcoeffs_array[positions]))
                else:
                    coefficients.append(allcoeffs_array[i])

        # 1. ropa DF: indexes (positive or negative) and reaction names
        factor = [1.0 - 2.0*(coeff < 0) for coeff in coefficients]
        ropa_df = pd.DataFrame(np.array([factor, names], dtype=object).T,
                               index=indices, columns=['factor', 'reaction_names'])

        # SUM FORWARD AND BACKWARD (based on name)? WAS THERE IN PREVIOUS FUNCTION

        if rate_type == 'P':
            ropa_df = ropa_df[ropa_df['factor'].values > 0]
        elif rate_type == 'C':
            ropa_df = ropa_df[ropa_df['factor'] < 0]

        # 2. get reaction rates
        # if cumulative rate and ropa sign agree: don't change sign; otherwise, do
        rr = dict.fromkeys(ropa_df.index)
        rrsum = pd.Series(index=ropa_df.index, dtype=np.float64)

        for idx in ropa_df.index:
            rr_idx = np.array(self.GetReactionRates(reaction_index=[idx])[0])
            rrsum_idx = np.trapz(y=rr_idx, x=xaxis)
            if (rrsum_idx * float(ropa_df['factor'][idx])) < 0:
                # integral and ropa have opposite signs: change sign
                rr_idx *= -1
                rrsum_idx *= -1
            # assign index
            rr[idx] = rr_idx
            rrsum[idx] = rrsum_idx

        # check cumulative contribution and delete based on threshold
        rrsum /= np.sum(abs(rrsum))  # abs?
        filteredidxs = list(rrsum[abs(rrsum) > threshold].index)
        filtered_rr = [rr[key] for key in filteredidxs]

        # add to the names the cumulative % contribution
        names_wpct = []
        for idx in filteredidxs:
            name = ropa_df['reaction_names'][idx]
            pct = rrsum[idx] * 100
            names_wpct.append('{} {:.2f}%'.format(name, pct))
        cumulativerates_df = pd.DataFrame(np.array(filtered_rr).T, columns=names_wpct, index=xaxis)

        return cumulativerates_df

# alternative : do a local ropa to set values; if you don't find the reaction,
# set the value to zero
