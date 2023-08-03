import os
import xml.etree.ElementTree as ET
import numpy as np

'''
MODULE: KineticMechanism
@Authors:
    Alberto Cuoci [1], Timoteo Dinelli [1], Luna Pratali Maffei[1]
    [1]: CRECK Modeling Lab, Department of Chemistry, Materials, and Chemical Engineering, Politecnico di Milano
@Contacts:
    alberto.cuoci@polimi.it
    timoteo.dinelli@polimi.it
    luna.pratalimaffei@polimi.it
@Additional notes:
    - This code is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
      Please report any bug to: alberto.cuoci@polimi.it
    - This is a modified class frome the original one KineticMechanism.py inside PyTools4OpenSMOKE 
      modified by Timoteo Dinelli to handle gas-phase only to post-process data
      in order to integrate the entire capability of post-processing
      simulations inside the pySMOKEPostProcessor.
    - Luna Pratali Maffei add utilities to perform post processing of reaction classes
'''

class KineticMap:

    def __init__(self, KineticFolder: str):

        reactionNames_xml = os.path.join(KineticFolder, "reaction_names.xml")
        kinetic_xml = os.path.join(KineticFolder, "kinetics.xml")
        
        reaction_names_tree = ET.parse(reactionNames_xml) # rn
        rn_root = reaction_names_tree.getroot()

        self.reaction_names = rn_root.find("reaction-names")
        self.reaction_names = (self.reaction_names.text).split()

        tree = ET.parse(kinetic_xml)
        root = tree.getroot()
    
        # List of elements
        elements = root.find('NamesOfElements')
        elements = (elements.text).split()
        NumberOfElements = len(elements) # ne

        # List of species
        species = root.find('NamesOfSpecies')
        species = (species.text).split()
        NumberOfSpecies = len(species) # ns

        # Elemental composition
        atomic = root.find('AtomicComposition')
        atomic = (atomic.text).split()
        atomic = np.reshape(atomic, (NumberOfSpecies, NumberOfElements))
        atomic = np.float32(atomic)
        
        # Elements molecular weights
        mwe = []
        """
        This values are taken from OpenSMOKEpp library 'kernel/thermo/AtomicElementMap.hpp'
        """
        for elem in elements:
            if (elem == 'C'): 
                self.iC = elements.index('C')
                mwe.append(12.010999679565430)
            if (elem == 'H'): 
                self.iH = elements.index('H')
                mwe.append(1.008000016212463)
            if (elem == 'O'): 
                self.iO = elements.index('O')
                mwe.append(15.998999595642090)
            if (elem == 'N'): 
                self.iN = elements.index('N')
                mwe.append(14.0069999694824)
            if (elem == 'HE'): 
                self.iHE = elements.index('HE')
                mwe.append(4.002999782562256)
            if (elem == 'AR'): 
                self.iAR = elements.index('AR')
                mwe.append(39.948001861572270)
            if (elem == 'S'): 
                self.iS = elements.index('S')
                mwe.append(32.065)
        mwe = np.array(mwe)
        
        # Species molecular weights
        mws = atomic.dot(mwe)
        
        # Soot classes (if they exists)
        # This is for postprocessing soot (currently not implemented)
        # reaction_class_name = []
        # reaction_class_size = []
        # reaction_class_indices = []
        
        # Reading kinetics
        kinetics = root.find('Kinetics')
        
        # Number Of Reactions
        NumberOfReactions = int( (kinetics.find('NumberOfReactions')).text ) # nr
        
        # Fall Off reactions
        FallOff = ((kinetics.find("FallOff")).text).split()
        self.NumberOfFallOffReactions = int(FallOff[0])
        listIndicesOfFallOffReactions = FallOff[1:]
        self.IndicesOfFallOffReactions = [int(i) for i in listIndicesOfFallOffReactions]

        # Cabr Reactions
        Cabr = ((kinetics.find("CABR")).text).split()
        self.NumberOfCabrReactions = int(Cabr[0])
        listIndicesOfCabrReactions = Cabr[1:]
        self.IndicesOfCabrReactions = [int(i) for i in listIndicesOfCabrReactions]

        # Kinetic parameters
        kinetic_parameters = kinetics.find('KineticParameters')
        direct = kinetic_parameters.find('Direct')
        
        lnA = direct.find('lnA')
        lnA = (lnA.text).split()
        lnA = np.float64(lnA[1:])
        A = np.exp(lnA)
        
        Beta = direct.find('Beta')
        Beta = (Beta.text).split()
        Beta = np.float64(Beta[1:])
        
        E_over_R = direct.find('E_over_R')
        E_over_R = (E_over_R.text).split()
        E_over_R = np.float64(E_over_R[1:])

        
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
        
        self.groups = []

        self.A = A
        self.Beta = Beta
        self.E_over_R = E_over_R
        
        self.reactions = []

    def Classes(self):
        """ read reaction classes if present
        """
        reaction_classes = self.kinetics.find('ReactionClasses')
        self.rxnclass = dict.fromkeys(np.arange(1, self.NumberOfReactions+1))
        self.rxnsubclass = dict.fromkeys(np.arange(1, self.NumberOfReactions+1))
        
        if (reaction_classes != None):
            # classes: {mainclass: {subclass: [indices]}}
            classes = {}
            for child in reaction_classes:
                if (child.tag == 'MainClass'):
                    classname = child.attrib['name']
                    if classname not in list(classes.keys()):
                        # initialize
                        classes[classname] = {}
                    for subclass in child:
                        #if (subclass.tag == 'SubClass'): # should only contain subclass type
                        subclassname = subclass.attrib['name']
                        if subclassname not in list(classes[classname].keys()):
                            classes[classname][subclassname] = []
                        for subsec in subclass:
                            if (subsec.tag == 'ReactionIndices'):
                                dummy = (subsec.text).split()
                                
                                for i in dummy: # assign rxn indices
                                    i = int(i) +1
                                    classes[classname][subclassname].append(i)
                                    self.rxnclass[i] = classname
                                    self.rxnsubclass[i] = subclassname
            self.classes = classes
        else:
            raise Exception('The kinetic mechanism provided does not contain any reaction class!')
   
    def ReactionNameFromIndex(self, reactionIndex: int):
        # reactionIndex 0-based
        if(reactionIndex + 1 <= self.NumberOfReactions):
            name = "R" + str(reactionIndex + 1) + ": " + self.reaction_names[reactionIndex]
            return name
        else:
            local_index = reactionIndex + 1 - self.NumberOfReactions
            if(local_index <= self.NumberOfFallOffReactions):
                global_index = self.IndicesOfFallOffReactions[local_index - 1]
                name = "R" + str(global_index) + "(inf): " + self.reaction_names[global_index - 1]
                return name
            else:
                global_index = self.IndicesOfCabrReactions[local_index - self.NumberOfReactions - 1]
                name = "R" + str(global_index) + "(inf): " + self.reaction_names[global_index - 1]
                return name
    
    def ReactionIndexFromName(self, name: str):
        for i in range(0, len(self.reaction_names)):
            if(name == self.reaction_names[i]):
                return i # this is the index of the reaction 0-based pay attention to cabr and falloff reactions 
        
    def SpeciesNameFromIndex(self, speciesIndex: int):
        return self.species[speciesIndex]
    
    def IndexFromSpeciesName(self, speciesName: str):
        for i in range(0, self.NumberOfSpecies):
            if(speciesName == self.species[i]):
                return i

