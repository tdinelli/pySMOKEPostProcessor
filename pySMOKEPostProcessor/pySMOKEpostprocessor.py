import os
from ctypes import c_bool, c_int, c_double, c_void_p, c_char_p, byref, cdll
from pySMOKEPostProcessor.maps.KineticMap import KineticMap
from pySMOKEPostProcessor.maps.OpenSMOKEppXMLFile import OpenSMOKEppXMLFile
from pySMOKEPostProcessor.GraphWriter import GraphWriter

"""
DESCRIPTION: TODO
"""

class pySMOKEpostprocessor:

    def CheckInputSettings(self):

        if not(os.path.isdir(self.kineticFolder)):
            raise ValueError(
                'The folder for the kinetic mechanism does not exist')
        if not (os.path.isdir(self.outputFolder)):
            raise ValueError(
                'The folder for the simulation\'s results does not exist')

        kin = os.path.join(self.kineticFolder, b'kinetics.xml')
        names = os.path.join(self.kineticFolder, b'reaction_names.xml')
        output = os.path.join(self.outputFolder, b'Output.xml')
        outputsens = os.path.join(self.outputFolder, b'Sensitivities.xml')

        if not(os.path.isfile(kin)):
            raise ValueError(
                'The folder for the kinetic mechanism does not contains kinetics.xml file')
        if not(os.path.isfile(names)):
            raise ValueError(
                'The folder for the kinetic mechanism does not contains reaction-names.xml file')
        if not(os.path.isfile(output)):
            raise ValueError(
                'The folder for the simulation results does not contains Output.xml file')

        if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output) and self.verbose != False):
            print('ROPA available')
        if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output) and os.path.isfile(outputsens) and self.verbose != False):
            print('Sensitivity analysis available on: ', end='')
            for i in os.listdir(self.outputFolder):
                file = i.split(b'.')
                if (file[0] == b'Sensitivities' and file[1] != b'xml' and self.verbose != False):
                    print(str(file[1], encoding='utf-8'), end='  ')
            print(end="\n")

    def __init__(self, kinetic_mechanism: str, results_folder: str, verbose=False):

        path = os.path.join(os.getcwd(), '..', 'build', 'pySMOKEPostProcessor.o')
        self.kineticFolder = bytes(kinetic_mechanism, 'utf-8')
        self.outputFolder = bytes(results_folder, 'utf-8')
        self.verbose = verbose
        self.CheckInputSettings()

        self.c_library = cdll.LoadLibrary(path)
        if self.verbose:

            self.c_library.getBoundary.argtypes = [c_char_p,  # kinetic folder
                                                    c_char_p, # output folder
                                                    c_void_p, # domain max
                                                    c_void_p, # domain minimum
                                                    c_void_p] # domain middle point

            self.c_library.getBoundary.restype = c_int

            domain_maximum = (c_double*1)()
            domain_minimum = (c_double*1)()
            domain_middle = (c_double*1)()

            code = self.c_library.getBoundary ( c_char_p(self.kineticFolder), # kinetic folder
                                                c_char_p(self.outputFolder),  # output folder
                                                byref(domain_maximum),        # domain max
                                                byref(domain_minimum),        # domain minimum
                                                byref(domain_middle))         # domain middle point

            domain_maximum = [i for i in domain_maximum][0]
            domain_minimum = [i for i in domain_minimum][0]
            domain_middle = [i for i in domain_middle][0]

            print(f"Computational domain: \n * Lower Bound: {round(domain_minimum,6)}   Upper Bound: {round(domain_maximum, 6)}")
            print(f" * Middle value: {round(domain_middle)}")
            out = OpenSMOKEppXMLFile(kineticFolder = self.kineticFolder.decode("utf-8"),
                                    OutputFolder = self.outputFolder.decode("utf-8"))
            print("Available quantities for the abscissae variable:")
            for i in out.additional_variable:
                print(f" * {i}")
            print(" * All the mass fraction of the species inside the scheme (e.g. H2 or O2)")
    
    def RateOfProductionAnalysis(self, specie: str, ropa_type: str, local_value: float = 0,
                                 lower_value: float = 0, upper_value: float = 0,
                                 number_of_reactions: int = 10):
        specie = bytes(specie, 'utf-8')
        if (ropa_type == 'global'):
            ropa = 1
        elif (ropa_type == "local"):
            ropa = 0
        elif (ropa_type == "region"):
            ropa = 2
        else:
            raise ValueError('Please select one of the available ROPA type: global | local | region')

        self.c_library.pyROPAPostProcessor.argtypes = [c_char_p,  # kinetic folder
                                                       c_char_p,  # output folder
                                                       c_char_p,  # sepcie
                                                       c_int,     # ropa type 0: local | 1: global | 2: region
                                                       c_int,     # ordering type 0: peakvalues | 1: area | 2: absolutearea (it is not needed for ROPA just to have a single function in cpp)
                                                       c_int,     # normalization type 0: local | 1: maxvalue (it is not needed for ROPA just to have a single function in cpp)
                                                       c_double,  # ropa local value
                                                       c_double,  # ropa region lower value
                                                       c_double,  # ropa region upper value
                                                       c_void_p,  # ropa coefficients
                                                       c_void_p,  # ropa reactions indices
                                                       c_int]     # ropa number of reactions

        self.c_library.pyROPAPostProcessor.restype = c_int

        coefficients = (c_double * number_of_reactions)()
        reactions = (c_int * number_of_reactions)()

        code = self.c_library.pyROPAPostProcessor(c_char_p(self.kineticFolder), # kinetic folder
                                                  c_char_p(self.outputFolder),  # output folder
                                                  c_char_p(specie),             # specie
                                                  c_int(ropa),                  # ropa type 0: local | 1:global | 2: region
                                                  c_int(0),                     # ordering type 0: peakvalues | 1: area | 2: absolutearea (it is not needed for ROPA just to have a single function in cpp)
                                                  c_int(0),                     # normalization type 0: local | 1: maxvalue (it is not needed for ROPA just to have a single function in cpp)
                                                  c_double(local_value),        # ropa local value
                                                  c_double(lower_value),        # ropa region lower value
                                                  c_double(upper_value),        # ropa region upper value
                                                  byref(coefficients),          # ropa coefficients
                                                  byref(reactions),             # ropa reactions indices
                                                  c_int(number_of_reactions))   # ropa number of reactions

        # 0-based
        # reaction-names 1-based
        reaction_names = []
        KineticMap_ = KineticMap(self.kineticFolder.decode("utf-8"))
        for i in reactions:
            reaction_names.append(KineticMap_.ReactionNameFromIndex(i))

        if (code == 0):
            if(self.verbose != False):
                print('ROPA successfully executed!')
            coefficients = [c for c in coefficients]
            reactions = [r for r in reactions]
            return coefficients, reactions, reaction_names
        else:
            raise ValueError('exit code != 0')  # TODO

    def SensitivityAnalysis(self, target: str, sensitivity_type: str, ordering_type: str,
                            normalization_type: str, local_value: float = 0,
                            lower_value: float = 0, upper_value: float = 0,
                            number_of_reactions: int = 10):
        target = bytes(target, 'utf-8')
        if (sensitivity_type == 'global'):
            sensitivity = 1
        elif (sensitivity_type == "local"):
            sensitivity = 0
        elif (sensitivity_type == "region"):
            sensitivity = 2
        else:
            raise ValueError('Please select one of the available Sensitivity analysis type global | local | region')

        if (ordering_type == 'peak_value'):
            ordering = 0
        elif (ordering_type == "area"):
            ordering = 1
        elif (ordering_type == "absolute_area"):
            ordering = 2
        else:
            raise ValueError('Please select one of the available ordering type: peak_value | area | absolute_area')

        if (normalization_type == 'local'):
            normalization = 0
        elif (normalization_type == 'max_value'):
            normalization = 1
        else:
            raise ValueError('Please select one of the available normalization: local | max_value')

        self.c_library.pySensitivityPostProcessor.argtypes = [c_char_p,  # kinetic folder
                                                              c_char_p,  # output folder
                                                              c_char_p,  # target
                                                              c_int,     # sensitivity type 0: local | 1: global | 2: region
                                                              c_int,     # ordering type 0: peakvalues | 1: area | 2: absolutearea
                                                              c_int,     # normalization type 0: local | 1: maxvalue
                                                              c_double,  # sensitivity local value
                                                              c_double,  # sensitivity region lower value
                                                              c_double,  # sensitivity region upper value
                                                              c_void_p,  # sensitivity coefficients
                                                              c_void_p,  # reactions indices
                                                              c_int]     # sensitivity number of reactions

        self.c_library.pySensitivityPostProcessor.restype = c_int

        coefficients = (c_double * number_of_reactions)()
        reactions = (c_int * number_of_reactions)()

        code = self.c_library.pySensitivityPostProcessor(c_char_p(self.kineticFolder),  # kinetic folder
                                                        c_char_p(self.outputFolder), # output folder
                                                        c_char_p(target), # target
                                                        c_int(sensitivity), # sensitivity type 0: local | 1: global | 2: region
                                                        c_int(ordering), # ordering type 0: peakvalues | 1: area | 2: absolutearea
                                                        c_int(normalization), # normalization type 0: local | 1: maxvalue
                                                        c_double(local_value), # sensitivity local value
                                                        c_double(lower_value), # sensitivity region lower value
                                                        c_double(upper_value), # sensitivity region upper value
                                                        byref(coefficients), # sensitivity coefficients
                                                        byref(reactions), # reactions indices
                                                        c_int(number_of_reactions)) # sensitivity number of reactions

        # 0-based
        # reaction-names 1-based
        reaction_names = []
        KineticMap_ = KineticMap(self.kineticFolder.decode("utf-8"))
        for i in reactions:
            reaction_names.append(KineticMap_.ReactionNameFromIndex(i))

        if (code == 0):
            if(self.verbose != False):
                print('Sensitivity analysis succesfully executed!')
            coefficients = [c for c in coefficients]
            reactions = [r for r in reactions]
            return coefficients, reactions, reaction_names
        else:
            raise ValueError('exit code != 0')  # TODO

    def FluxAnalysis(self, specie: str, element: str, flux_analysis_type: str,
                     thickness: str, thickness_log_scale: bool,
                     label_type: str, depth: int = 2, width: int = 5,
                     threshold: float = 0, local_value: float = 0.01):
        specie = bytes(specie, 'utf-8')
        element = bytes(element, 'utf-8')

        if(flux_analysis_type == 'production'):
            flux = 1
        elif(flux_analysis_type == 'destruction'):
            flux = 0
        else:
            raise ValueError("The available type for the flux analysis are production | destruction")

        if(thickness == 'absolute'):
            thick = 0
        elif(thickness == 'relative'):
            thick = 1
        else:
            raise ValueError("The available type for the caluclation of the thicknsss are absolute | relative(%)")

        if(label_type == 'absolute'):
            label = 0
        elif(label_type == 'relative'):
            label = 1
        else:
            raise ValueError("The available type for the labeling are absolute | relative(%)")

        self.c_library.FluxAnalysis.argtypes = [c_char_p,  # kinetic folder
                                                c_char_p,  # output folder
                                                c_char_p,  # specie
                                                c_char_p,  # element
                                                c_int,     # flux analysis type
                                                c_double,  # ropa local value
                                                c_int,     # thickness 0 absolute | 1 relative(%)
                                                c_bool,    # thickness log scale
                                                c_int,     # labeling type 0 absolute | 1 relative(%)
                                                c_int,     # depth
                                                c_int,     # width
                                                c_double,  # thresold
                                                c_void_p,  # indexes of the first name
                                                c_void_p,  # indexes of the second name
                                                c_void_p,  # computed thicknes value
                                                c_void_p,  # computed label value
                                                c_void_p]  # lenght of the vector to adjust (boring ctype stuff)

        self.c_library.FluxAnalysis.restype = c_int

        indexFirstName = (c_int * 1000)()
        indexSecondName = (c_int * 1000)()
        computedThickness = (c_double * 1000)()
        computedLabel = (c_double * 1000)()
        length = (c_int*1000)()

        code = self.c_library.FluxAnalysis(c_char_p(self.kineticFolder), # kinetic folder
                                            c_char_p(self.outputFolder), # output folder
                                            c_char_p(specie),			 # specie
                                            c_char_p(element),			 # element
                                            c_int(flux), # flux analysis type
                                            c_double(local_value), # ropa local value
                                            c_int(thick), # thickness 0 absolute | 1 relative(%)
                                            c_bool(thickness_log_scale), # thickness log scale
                                            c_int(label), # labeling type 0 absolute | 1 relative(%)
                                            c_int(depth), # depth
                                            c_int(width), # width
                                            c_double(threshold), # threshold
                                            byref(indexFirstName), # indexes of the first name
                                            byref(indexSecondName), # indexes of the second name
                                            byref(computedThickness), # computed thicknes value
                                            byref(computedLabel), # computed label value
                                            byref(length)) # lenght of the vector to adjust (boring ctype stuff)

        length = [l for l in length][0]
        indexFirstName = [i for i in indexFirstName][:length]
        indexSecondName = [i for i in indexSecondName][:length]
        computedThickness = [t for t in computedThickness][:length]
        computedLabel = [l for l in computedLabel][:length]

        self.firstNames = []
        self.secondNames = []
        KineticMap_ = KineticMap(self.kineticFolder.decode("utf-8"))

        for j in range(len(indexFirstName)):
            self.firstNames.append( KineticMap_.SpecieNameFromIndex(indexFirstName[j]))
            self.secondNames.append(KineticMap_.SpecieNameFromIndex(indexSecondName[j]))

        Graph = GraphWriter(flux_analysis_type)
        Graph = Graph.CreateGraph(self.firstNames, self.secondNames, computedThickness, computedLabel)

        return Graph

    def ReactionRates(self, abscissae_name: str, reaction_name: str):
        
        kin = KineticMap(self.kineticFolder.decode("utf-8"))
        out = OpenSMOKEppXMLFile(kineticFolder = self.kineticFolder.decode("utf-8"), 
                                OutputFolder = self.outputFolder.decode("utf-8"))
        
        valid_x_name = out.additional_variable
        number_of_abscissae = out.npts

        x_axis_name = ''
        for i in valid_x_name:
            if abscissae_name in i:
                x_axis_name = bytes(i, 'utf-8')
        
        if (x_axis_name == ''): raise Exception('The provided name for the x axis is not valid')

        x_axis = out.getProfile(name = x_axis_name.decode('utf-8'))

        reaction_index = kin.ReactionIndexFromName(name = reaction_name)

        self.c_library.GetReactionRates.argtypes = [c_char_p, # kinetic folder
                                                    c_char_p, # output folder
                                                    c_int,    # reaction index
                                                    c_void_p] # reaction rate [kmol/m3/s]

        reaction_rate = (c_double * number_of_abscissae)()
        self.c_library.GetReactionRates.restype = c_int

        code = self.c_library.GetReactionRates(c_char_p(self.kineticFolder), # kinetic folder
                                                c_char_p(self.outputFolder), # output folder
                                                c_int(reaction_index),       # reaction index
                                                byref(reaction_rate))        # reaction rate

        if code != 0:
            raise ValueError('Exit code != 0')
        else:
            rr = [i for i in reaction_rate]
            return x_axis, rr