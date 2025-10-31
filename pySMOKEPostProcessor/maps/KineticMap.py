# ---------------------------------------------------------------------------------- #
#                                                                                    #
#                              _____  __  ___ ____   __ __  ______                   #
#                ____   __  __/ ___/ /  |/  // __ \ / //_/ / ____/____   ____        #
#               / __ \ / / / /\__ \ / /|_/ // / / // ,<   / __/  / __ \ / __ \       #
#              / /_/ // /_/ /___/ // /  / // /_/ // /| | / /___ / /_/ // /_/ /       #
#             / .___/ \__, //____//_/  /_/ \____//_/ |_|/_____// .___// .___/        #
#            /_/     /____/                                   /_/    /_/             #
#                                                                                    #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
# Please refer to the copyright statement and license                                #
# information at the end of this file.                                               #
# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Authors: Timoteo Dinelli     <timoteo.dinelli@polimi.it>                   #
#                  Luna Pratali Maffei <luna.pratali@polimi.it>                      #
#                  Edoardo Ramalli     <edoardo.ramalli@polimi.it>                   #
#                  Andrea Nobili       <edoardo.ramalli@polimi.it>                   #
#                                                                                    #
#         CRECK Modeling Group <http://creckmodeling.chem.polimi.it>                 #
#         Department of Chemistry, Materials and Chemical Engineering                #
#         Politecnico di Milano, P.zza Leonardo da Vinci 32, 20133 Milano            #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
import os
import xml.etree.ElementTree as ET
import numpy as np


class KineticMap:

    def __init__(self, kinetic_folder: str) -> None:

        reaction_names_xml = os.path.join(kinetic_folder, "reaction_names.xml")
        if not os.path.isfile(reaction_names_xml):
            raise ValueError("The kinetic folder does not contain any reaction_names.xml file!")

        kinetic_xml = os.path.join(kinetic_folder, "kinetics.xml")
        if not os.path.isfile(kinetic_xml):
            raise ValueError("The kinetic folder does not contain any kinetics.xml file!")

        self._reaction_names = self.parse_reaction_names(reaction_names_xml=reaction_names_xml)
        self.parse_kinetic(kinetics_xml=kinetic_xml)

    @staticmethod
    def parse_reaction_names(reaction_names_xml: str) -> list:
        """
        Function that parse the XML file named reaction_names.xml
        Args:
            reaction_names_xml (str): complete path to the file named reaction_names.xml.
        Returns:
            (list): list of string containing the names of all the reactions inside a mechanism.
        """
        reaction_names_tree = ET.parse(reaction_names_xml)
        rn_root = reaction_names_tree.getroot()
        reaction_names = rn_root.find("reaction-names")
        reaction_names = (reaction_names.text).split()
        return reaction_names

    def parse_kinetic(self, kinetics_xml: str) -> None:
        """
        Function that parses the file named kinetics.xml extrating all the informations contained within the mechanism.
        Args:
            kinetics_xml (str): complete path to the file named kinetics.xml.
        """
        tree = ET.parse(kinetics_xml)
        root = tree.getroot()

        # List of elements
        elements = root.find("NamesOfElements").text.split()
        number_of_elements = len(elements)  # ne

        # List of species
        species = root.find("NamesOfSpecies").text.split()
        number_of_species = len(species)  # ns

        # Atomic composition
        atomic = np.fromstring(root.find("AtomicComposition").text, dtype=np.float32, sep=" ")
        atomic = atomic.reshape((number_of_species, number_of_elements))

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

        # Kinetics
        kinetics = root.find("Kinetics")

        # Number Of Reactions
        number_of_reactions = int(kinetics.findtext("NumberOfReactions"))

        # Fall Off reactions
        self._number_of_falloff_reactions, *indices_of_falloff_reactions = map(
            int, kinetics.find("FallOff").text.split()
        )
        self._indices_of_falloff_reactions = indices_of_falloff_reactions

        # Cabr Reactions
        self._number_of_cabr_reactions, *indices_of_cabr_reactions = map(int, kinetics.find("CABR").text.split())
        self._indices_of_cabr_reactions = indices_of_cabr_reactions

        # Kinetic parameters
        kinetic_parameters = kinetics.find("KineticParameters")
        direct = kinetic_parameters.find("Direct")

        self._A = np.exp(np.fromstring(direct.findtext("lnA"), dtype=np.float64, sep=" ")[1:])
        self._Beta = np.fromstring(direct.findtext("Beta"), dtype=np.float64, sep=" ")[1:]
        self._E_over_R = np.fromstring(direct.findtext("E_over_R"), dtype=np.float64, sep=" ")[1:]

        self._elements = elements
        self._atomic = atomic
        self._species = species
        self._number_of_elements = number_of_elements
        self._number_of_species = number_of_species
        self._number_of_reactions = number_of_reactions
        self._kinetics = kinetics

        self._mwe = mwe
        self._mws = mws

    def read_reactionclasses(self) -> dict:
        """
        Read reaction classes if present, within the kinetic mechanism, requires the scheme to be compiled with
        OpenSMOKE version >= 0.20.0.
        Raises:
            Exception: If no reaction classes definitions found raise exception.
        """
        reaction_classes = self._kinetics.find("ReactionClasses")

        if reaction_classes is None:
            raise Exception("The kinetic mechanism provided does not contain any reaction class!")

        reaction_class = {i: None for i in range(1, self._number_of_reactions + 1)}
        reaction_subclass = {i: None for i in range(1, self._number_of_reactions + 1)}
        classes = {}

        for child in reaction_classes:
            if child.tag == "MainClass":
                classname = child.attrib["name"]
                class_entry = classes.setdefault(classname, {})

                for subclass in child:
                    subclassname = subclass.attrib["name"]
                    subclass_entry = class_entry.setdefault(subclassname, [])
                    reaction_indices = subclass.find("ReactionIndices")
                    if reaction_indices is not None:
                        indices = map(int, reaction_indices.text.split())
                        for i in indices:
                            i += 1
                            subclass_entry.append(i)
                            reaction_class[i] = classname
                            reaction_subclass[i] = subclassname
        print(reaction_class)

        return classes

    def reaction_name_from_index(self, reaction_index: int) -> str:
        """
        Function that given the index of a reaction returns its name.
        Args:
            reaction_index (int): Index of the reaction (0-based).
        Returns:
            (str): Name of the reaction.
        """
        if reaction_index < self._number_of_reactions:
            return f"R{reaction_index + 1}: {self._reaction_names[reaction_index]}"
        elif reaction_index < self._number_of_reactions + self._number_of_falloff_reactions:
            global_index = self._indices_of_falloff_reactions[reaction_index - self._number_of_reactions]
            return f"R{global_index}(inf): {self._reaction_names[global_index - 1]}"
        else:
            global_index = self._indices_of_cabr_reactions[
                reaction_index - self._number_of_reactions - self._number_of_falloff_reactions
            ]
            return f"R{global_index}(inf): {self._reaction_names[global_index - 1]}"

    def reaction_index_from_name(self, name: str) -> int:
        """
        Function that given the name of the reaction returns the corresponding index whithin the list of the reactions.
        Warning: this is the index of the reaction 0-based pay attention to cabr and falloff reactions.
        Args:
            name (str): reaction name.
        Returns:
            (int): index of the reaction.
        """
        try:
            return self._reaction_names.index(name)
        except ValueError:
            raise ValueError(f"The requested reaction {name} is not available whithin the kinetic mechanism")

    def species_name_from_index(self, index: int) -> str:
        """
        Function that given an index returns the coressponding species name.
        Args:
            index (int): Species index.
        Returns:
            (str): name of the species.
        """
        if 0 <= index < len(self._species):
            return self._species[index]
        else:
            raise IndexError(f"Index {index} out of range")

    def index_from_species_name(self, name: str) -> int:
        """
        Function that given the name of a species returns its index.
        Args:
            name: species name.
        Returns:
            Index of the species.
        """
        try:
            return self._species.index(name)
        except ValueError:
            raise ValueError(f"The kinetic mechanism does not contain the requested species {name}!")

    @property
    def elements(self):
        return self._elements

    @property
    def atomic(self):
        return self._atomic

    @property
    def species(self):
        return self._species

    @property
    def number_of_elements(self):
        return self._number_of_elements

    @property
    def number_of_species(self):
        return self._number_of_species

    @property
    def number_of_reactions(self):
        return self._number_of_reactions

    @property
    def mwe(self):
        return self._mwe

    @property
    def mws(self):
        return self._mws

    @property
    def A(self):
        return self._A

    @property
    def Beta(self):
        return self._Beta

    @property
    def E_over_R(self):
        return self._E_over_R

    @property
    def number_of_falloff_reactions(self):
        return self._number_of_falloff_reactions

    @property
    def indices_of_falloff_reactions(self):
        return self._indices_of_falloff_reactions

    @property
    def number_of_cabr_reactions(self):
        return self._number_of_cabr_reactions

    @property
    def indices_of_cabr_reactions(self):
        return self._indices_of_cabr_reactions
# ---------------------------------------------------------------------------------- #
#                                                                                    #
#         Python wrapper around the OpenSMOKEpp Graphical Post Processor.            #
#         Copyright (C) 2024                                                         #
#             Timoteo Dinelli     <timoteo.dinelli@polimi.it>                        #
#             Luna Pratali Maffei <luna.pratali@polimi.it>                           #
#             Edoardo Ramalli     <edoardo.ramalli@polimi.it>                        #
#             Andrea Nobili       <anobili@stanford.edu>                             #
#                                                                                    #
#         This program is free software: you can redistribute it and/or modify       #
#         it under the terms of the GNU General Public License as published by       #
#         the Free Software Foundation, either version 3 of the License, or          #
#         (at your option) any later version.                                        #
#                                                                                    #
#         This program is distributed in the hope that it will be useful,            #
#         but WITHOUT ANY WARRANTY; without even the implied warranty of             #
#         MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the              #
#         GNU General Public License for more details.                               #
#                                                                                    #
#         You should have received a copy of the GNU General Public License          #
#         along with this program.  If not, see <https://www.gnu.org/licenses/>.     #
#                                                                                    #
# ---------------------------------------------------------------------------------- #
