import os
import xml.etree.ElementTree as ET

import numpy as np

"""
Dev NOTES: I am thinking of removing this class and OpenSMOKEppXML class in the same folder in favour of
          OpenSMOKEpp_Interfaces package keep in mind this in case of future refactoring.
MODULE: KineticMechanism
@Authors:
    Alberto Cuoci [1], Timoteo Dinelli [1], Luna Pratali Maffei [1]
    [1]: CRECK Modeling Lab, Department of Chemistry, Materials, and Chemical Engineering, Politecnico di Milano
@Contacts:
    alberto.cuoci@polimi.it
    timoteo.dinelli@polimi.it
    luna.pratalimaffei@polimi.it
@Additional notes:
    - This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
      Please report any bug to: timoteo.dinelli@polimi.it
    - This is a modified class frome the original one KineticMechanism.py inside PyTools4OpenSMOKE modified by
      Timoteo Dinelli to handle gas-phase in order to post-process data in order to integrate the entire capability of
      post-processing simulations inside the pySMOKEPostProcessor. Improved performances to make it runs blazingly fast.
    - Luna Pratali Maffei add utilities to perform post processing of reaction classes
"""


class KineticMap:
    def __init__(self, KineticFolder: str):
        reactionNames_xml = os.path.join(KineticFolder, "reaction_names.xml")
        if not os.path.isfile(reactionNames_xml):
            raise ValueError(
                "The kinetic folder does not contain any reaction_names.xml file! Please provide a valid mechanism"
            )

        kinetic_xml = os.path.join(KineticFolder, "kinetics.xml")

        if not os.path.isfile(kinetic_xml):
            raise ValueError(
                "The kinetic folder does not contain any kinetics.xml file! Please provide a valid mechanism"
            )

        self.ParseReactionNames(reaction_names=reactionNames_xml)
        self.ParseKinetic(kinetics_file=kinetic_xml)

    def ParseReactionNames(self, reaction_names: str) -> None:
        """
        Function that parse the reaction_names.xml file and define the necessary variables for the class.
        Args:
            reaction_names: path to the file reaction_names.xml.
        """
        reaction_names_tree = ET.parse(reaction_names)
        rn_root = reaction_names_tree.getroot()
        self.reaction_names = rn_root.find("reaction-names")
        self.reaction_names = (self.reaction_names.text).split()

    def ParseKinetic(self, kinetics_file: str) -> None:
        """
        Function that parse the kinetics.xml file and define the necessary variables for the class.
        Args:
            kinetics_file: path to the file kinetics.xml.
        """
        tree = ET.parse(kinetics_file)
        root = tree.getroot()

        # List of elements
        elements = root.find("NamesOfElements").text.split()
        NumberOfElements = len(elements)  # ne

        # List of species
        species = root.find("NamesOfSpecies").text.split()
        NumberOfSpecies = len(species)  # ns

        # Atomic composition
        atomic = np.fromstring(root.find("AtomicComposition").text, dtype=np.float32, sep=" ")
        atomic = atomic.reshape((NumberOfSpecies, NumberOfElements))

        # Elements molecular weights
        element_weights = {
            "C": 12.010999679565430,
            "H": 1.008000016212463,
            "O": 15.998999595642090,
            "N": 14.0069999694824,
            "HE": 4.002999782562256,
            "AR": 39.948001861572270,
            "S": 32.065,
        }

        mwe = np.array([element_weights.get(elem, 0.0) for elem in elements], dtype=np.float32)

        # Species molecular weights
        mws = np.dot(atomic, mwe)

        # Soot classes (if they exists)
        # This is for postprocessing soot (currently not implemented)
        # reaction_class_name = []
        # reaction_class_size = []
        # reaction_class_indices = []

        # Kinetics
        kinetics = root.find("Kinetics")

        # Number Of Reactions
        NumberOfReactions = int(kinetics.findtext("NumberOfReactions"))

        # Fall Off reactions
        self.NumberOfFallOffReactions, *IndicesOfFallOffReactions = map(int, kinetics.find("FallOff").text.split())
        self.IndicesOfFallOffReactions = IndicesOfFallOffReactions
        # Cabr Reactions
        self.NumberOfCabrReactions, *IndicesOfCabrReactions = map(int, kinetics.find("CABR").text.split())
        self.IndicesOfCabrReactions = IndicesOfCabrReactions

        # Kinetic parameters
        kinetic_parameters = kinetics.find("KineticParameters")
        direct = kinetic_parameters.find("Direct")

        self.A = np.exp(np.fromstring(direct.findtext("lnA"), dtype=np.float64, sep=" ")[1:])
        self.Beta = np.fromstring(direct.findtext("Beta"), dtype=np.float64, sep=" ")[1:]
        self.E_over_R = np.fromstring(direct.findtext("E_over_R"), dtype=np.float64, sep=" ")[1:]

        # Assign internal members

        self.elements = elements
        self.atomic = atomic
        self.species = species
        self.NumberOfElements = NumberOfElements
        self.NumberOfSpecies = NumberOfSpecies
        self.NumberOfReactions = NumberOfReactions
        self.kinetics = kinetics

        self.mwe = mwe
        self.mws = mws

        # TODO: Check here, these two variables seems to be unsed
        self.groups = []
        self.reactions = []

    def Classes(self) -> None:
        """
        Read reaction classes if present.
        Raises:
            Exception: If no reaction classes definitions found raise exception.
        """
        reaction_classes = self.kinetics.find("ReactionClasses")

        if reaction_classes is None:
            raise Exception("The kinetic mechanism provided does not contain any reaction class!")

        # TODO (TD): Luna PPM I don't really like the following two lines I am thinking on how to rewrite them better.
        self.rxnclass = dict.fromkeys(np.arange(1, self.NumberOfReactions + 1))
        self.rxnsubclass = dict.fromkeys(np.arange(1, self.NumberOfReactions + 1))
        classes = {}

        for child in reaction_classes:
            if child.tag == "MainClass":
                classname = child.attrib["name"]
                if classname not in classes:
                    classes[classname] = {}
                for subclass in child:
                    subclassname = subclass.attrib["name"]
                    if subclassname not in classes[classname]:
                        classes[classname][subclassname] = []
                    reaction_indices = subclass.find("ReactionIndices")
                    if reaction_indices is not None:
                        indices = map(int, reaction_indices.text.split())
                        for i in indices:
                            i += 1
                            classes[classname][subclassname].append(i)
                            self.rxnclass[i] = classname
                            self.rxnsubclass[i] = subclassname

        self.classes = classes

    def ReactionNameFromIndex(self, reactionIndex: int) -> str:
        """
        Function that given the index of a reaction returns its name.
        Args:
            reactionIndex: Index of the reaction (0-based).
        Returns:
            Name of the reaction.
        """
        if reactionIndex < self.NumberOfReactions:
            return f"R{reactionIndex + 1}: {self.reaction_names[reactionIndex]}"
        elif reactionIndex < self.NumberOfReactions + self.NumberOfFallOffReactions:
            global_index = self.IndicesOfFallOffReactions[reactionIndex - self.NumberOfReactions]
            return f"R{global_index}(inf): {self.reaction_names[global_index - 1]}"
        else:
            global_index = self.IndicesOfCabrReactions[
                reactionIndex - self.NumberOfReactions - self.NumberOfFallOffReactions
            ]
            return f"R{global_index}(inf): {self.reaction_names[global_index - 1]}"

    def ReactionIndexFromName(self, name: str) -> int:
        """
        Function that given the name of the reaction returns the corresponding index whithin the list of the reactions.
        Warning: this is the index of the reaction 0-based pay attention to cabr and falloff reactions.
        Args:
            name: reaction name.
        Returns:
            Index of the reaction.
        """
        try:
            return self.reaction_names.index(name)
        except ValueError:
            raise ValueError("The requested reaction is not available whithin the kinetic mechanism")

    def SpeciesNameFromIndex(self, index: int) -> str:
        """
        Function that given an index returns the coressponding species name.
        Args:
            index: Species index.
        Returns:
            Name of the species.
        """
        if 0 <= index < len(self.species):
            return self.species[index]
        else:
            raise IndexError("Index out of range")

    def IndexFromSpeciesName(self, name: str) -> int:
        """
        Function that given the name of a species returns its index.
        Args:
            name: species name.
        Returns:
            Index of the species.
        """
        try:
            return self.species.index(name)
        except ValueError:
            raise ValueError("The kinetic mechanism does not contain the requested species!")
