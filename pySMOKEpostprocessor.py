from ctypes import c_float, c_int, c_double, c_void_p, c_char_p, byref, cdll
import os

"""
DESCRIPTION: TODO
"""

class pySMOKEpostproccesor:
    
    def CheckInputSettings(self):

        if not( os.path.isdir(self.kineticFolder)):
            raise ValueError('The folder for the kinetic mechanism does not exist')
        if not (os.path.isdir(self.outputFolder)):
            raise ValueError('The folder for the simulation\'s results does not exist')
        
        kin = os.path.join(self.kineticFolder, b'kinetics.xml')
        names = os.path.join(self.kineticFolder, b'reaction_names.xml')
        output = os.path.join(self.outputFolder, b'output.xml')
        outputsens = os.path.join(self.outputFolder, b'Sensitivities.xml')

        if not(os.path.isfile(kin)):
            raise ValueError('The folder for the kinetic mechanism does not contains kinetics.xml file')
        if not(os.path.isfile(names)):
            raise ValueError('The folder for the kinetic mechanism does not contains reaction-names.xml file')
        if not(os.path.isfile(output)):
            raise ValueError('The folder for the simulation results does not contains output.xml file')
        
        if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output)):
            print('ROPA available')
        if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output) and os.path.isfile(outputsens)):
            print('Sensitivity analysis available on: ', end='')
            for i in  os.listdir(self.outputFolder):
                file = i.split(b'.')
                if (file[0] == b'Sensitivities' and file[1] != b'xml'):
                    print(str(file[1], encoding='utf-8'), end='  ')

    def __init__(self, kineticmechanismFolder: str, simulationresultsfolder: str):
        
        path = 'C:\\Users\\timot\\Desktop\\GitHub\\pyPostProcessor\\project\\x64\\Debug\\pySMOKEpostprocessor.dll'
        
        self.kineticFolder = bytes(kineticmechanismFolder, 'utf-8')
        self.outputFolder = bytes(simulationresultsfolder, 'utf-8')

        self.CheckInputSettings()

        self.c_library = cdll.LoadLibrary(path)

    def RateOfProductionAnalysis(self, specie: str, ropatype: str, ropalocalvalue: float = 0, 
                                roparegionlowervalue: float = 0, roparegionuppervalue: float = 0, 
                                numberofreactions: int = 10):
        specie = bytes(specie, 'utf-8')
        if (ropatype == 'global'):
            ropa = 1
        elif (ropatype == "local"):
            ropa = 0
        elif (ropatype == "region"):
            ropa = 2
        else:
            raise ValueError('Please select one of the available ROPA type: global | local | region')
        
        self.c_library.pyROPAPostProcessor.argtypes = [c_char_p, # kinetic folder
                                          c_char_p, # output folder
                                          c_char_p, # sepcie
                                          c_int,    # command
                                          c_int,    # ropa type 0: local | 1: global | 2: region
                                          c_double, # ropa local value
                                          c_double, # ropa region lower value
                                          c_double, # ropa region upper value
                                          c_void_p, # ropa coefficients
                                          c_void_p, # ropa reactions indices
                                          c_int]    # ropa number of reactions

        self.c_library.pyROPAPostProcessor.restype = c_int

        coefficients = (c_double * numberofreactions)()
        reactions = (c_int * numberofreactions)()

        code = self.c_library.pyROPAPostProcessor(c_char_p(self.kineticFolder), # kinetic folder
                                            c_char_p(self.outputFolder),        # output folder
                                            c_char_p(specie),                   # specie
                                            c_int(0),                           # command (to be removed)
                                            c_int(ropa),                        # ropa type 0: local | 1:global | 2: region
                                            c_double(ropalocalvalue),           # ropa local value
                                            c_double(roparegionlowervalue),     # ropa region lower value 
                                            c_double(roparegionuppervalue),     # ropa region upper value
                                            byref(coefficients),                # ropa coefficients
                                            byref(reactions),                   # ropa reactions indices
                                            c_int(numberofreactions))           # ropa number of reactions
                                            
        if (code == 0):
            print ('ROPA successfully executed')
            coefficients = [c for c in coefficients]
            reactions = [r for r in reactions]
            return coefficients, reactions
        else:
            raise ValueError('exit code != 0') # TODO

    def SensitivityAnalysis(self, specie: str, sensitivitytype: str, orderingtype:str,
                            normalizationtype:str, sensitivitylocalvalue: float = 0, 
                            sensitivityregionlowervalue: float = 0, sensitivityregionuppervalue: float = 0, 
                            numberofreactions: int = 10):
        specie = bytes(specie, 'utf-8')
        if (sensitivitytype == 'global'):
            sensitivity = 1
        elif (sensitivitytype == "local"):
            sensitivity = 0
        elif (sensitivitytype == "region"):
            sensitivity = 2
        else:
            raise ValueError('Please select one of the available Sensitivity analysis type global | local | region')
        
        if (orderingtype == 'peakvalues'):
            ordering = 0
        elif (orderingtype == "area"):
            ordering = 1
        elif (orderingtype == "absolutearea"):
            ordering = 2
        else: 
            raise ValueError('Please select one of the available ordering type: peakvalues | area | absolutearea')
        
        if (normalizationtype == 'local'):
            normalization = 0
        elif (normalizationtype == 'maxvalue'):
            normalization = 1
        else:
            raise ValueError('Please select one of the available normalization: local | maxvalue')

        self.c_library.pySensitivityPostProcessor.argtypes = [c_char_p, # kinetic folder
                                                c_char_p,  # output folder
                                                c_char_p,  # specie
                                                c_int,     # command
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

        coefficients = (c_double * numberofreactions)()
        reactions = (c_int * numberofreactions)()


        code = self.c_library.pySensitivityPostProcessor(c_char_p(self.kineticFolder), # kinetic folder
                                                    c_char_p(self.outputFolder),       # output folder
                                                    c_char_p(specie),                  # specie
                                                    c_int(0),                          # command
                                                    c_int(sensitivity),                # sensitivity type 0: local | 1: global | 2: region
                                                    c_int(ordering),                   # ordering type 0: peakvalues | 1: area | 2: absolutearea
                                                    c_int(normalization),              # normalization type 0: local | 1: maxvalue
                                                    c_double(sensitivitylocalvalue),       # sensitivity local value
                                                    c_double(sensitivityregionlowervalue), # sensitivity region lower value
                                                    c_double(sensitivityregionuppervalue), # sensitivity region upper value
                                                    byref(coefficients),                   # sensitivity coefficients
                                                    byref(reactions),                      # reactions indices
                                                    c_int(numberofreactions))              # sensitivity number of reactions
        
        if (code == 0):
            print('Sensitivity analysis succesfully executed')
            coefficients = [c for c in coefficients]
            reactions = [r for r in reactions]
            return coefficients, reactions
        else:
            raise ValueError('exit code != 0') # TODO