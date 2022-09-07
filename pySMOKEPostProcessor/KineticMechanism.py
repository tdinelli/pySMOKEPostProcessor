
import xml.etree.ElementTree as ET
import os

"""
DESCRIPTION: TODO
"""

class KineticMechanism:

    def __init__(self, kineticmechanismFolder: str):
    
        reactionNames = os.path.join(kineticmechanismFolder, "reaction_names.xml")
        kinetics = os.path.join(kineticmechanismFolder, "kinetics.xml")
        
        tree_kinetics = ET.parse(kinetics)
        root_kinetics = tree_kinetics.getroot()

        tree_names = ET.parse(reactionNames)
        root_names = tree_names.getroot()

        self.reaction_strings_ = root_names.find("reaction-names")
        self.reaction_strings_ = (self.reaction_strings_.text).split()

        specie = root_kinetics.find("NamesOfSpecies")
        self.specieNames = (specie.text).split()

        kinetics = root_kinetics.find("Kinetics")
        self.nr = int( (kinetics.find('NumberOfReactions')).text )
        
        FallOff = ((kinetics.find("FallOff")).text).split()
        self.NumberOfFallOffReactions = int(FallOff[0])
        listIndicesOfFallOffReactions = FallOff[1:]
        self.IndicesOfFallOffReactions = [int(i) for i in listIndicesOfFallOffReactions]

        Cabr = ((kinetics.find("CABR")).text).split()
        self.NumberOfCabrReactions = int(Cabr[0])
        listIndicesOfCabrReactions = Cabr[1:]
        self.IndicesOfCabrReactions = [int(i) for i in listIndicesOfCabrReactions] 
    
    def returnReactionNameFromIndex(self, reactionIndex: int):
        # reactionIndex 0-based
        if(reactionIndex <= self.nr):

            name = "R" + str(reactionIndex) + ": " + self.reaction_strings_[reactionIndex-1]
            return name
        else:

            local_index = reactionIndex - self.nr
            if(local_index <= self.NumberOfFallOffReactions):

                global_index = self.IndicesOfFallOffReactions[local_index-1]
                name = "R" + str(global_index) + "(inf): " + self.reaction_strings_[global_index-1]
                return name
            else:

                global_index = self.IndicesOfCabrReactions[local_index- self.nr - 1]
                name = "R" + str(global_index) + "(inf): " + self.reaction_strings_[global_index-1]
                return name
    
    def returnSpecieNameFromIndex(self, specieIndex: int):
        return self.specieNames[specieIndex]