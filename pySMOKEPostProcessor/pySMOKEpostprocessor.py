from ctypes import c_bool, c_int, c_double, c_void_p, c_char_p, byref, cdll
from KineticMechanism import KineticMechanism
from GraphWriter import GrapWirter
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
		output = os.path.join(self.outputFolder, b'Output.xml')
		outputsens = os.path.join(self.outputFolder, b'Sensitivities.xml')

		if not(os.path.isfile(kin)):
			raise ValueError('The folder for the kinetic mechanism does not contains kinetics.xml file')
		if not(os.path.isfile(names)):
			raise ValueError('The folder for the kinetic mechanism does not contains reaction-names.xml file')
		if not(os.path.isfile(output)):
			raise ValueError('The folder for the simulation results does not contains Output.xml file')

		if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output) and self.verbose != False):
			print('ROPA available')
		if (os.path.isfile(kin) and os.path.isfile(names) and os.path.isfile(output) and os.path.isfile(outputsens) and self.verbose != False):
			print('Sensitivity analysis available on: ', end='')
		for i in  os.listdir(self.outputFolder):
			file = i.split(b'.')
			if (file[0] == b'Sensitivities' and file[1] != b'xml' and self.verbose != False):
				print(str(file[1], encoding='utf-8'), end='  ')

	def __init__(self, kineticmechanismFolder: str, simulationresultsfolder: str, verbose = False):
        
		path = '/home/tdinelli/Documents/GitHub/pySMOKEPostProcessor/project/myLINUX/pySMOKEPostProcessor.o'
        
		self.kineticFolder = bytes(kineticmechanismFolder, 'utf-8')
		self.outputFolder = bytes(simulationresultsfolder, 'utf-8')
		self.verbose = verbose
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
                                          c_int,    # ropa type 0: local | 1: global | 2: region
										  c_int,    # ordering type 0: peakvalues | 1: area | 2: absolutearea (it is not needed for ROPA just to have a single function in cpp)
                                          c_int,    # normalization type 0: local | 1: maxvalue (it is not needed for ROPA just to have a single function in cpp)
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
                                            c_int(ropa),                        # ropa type 0: local | 1:global | 2: region
											c_int(0),							# ordering type 0: peakvalues | 1: area | 2: absolutearea (it is not needed for ROPA just to have a single function in cpp)
											c_int(0),							# normalization type 0: local | 1: maxvalue (it is not needed for ROPA just to have a single function in cpp)
                                            c_double(ropalocalvalue),           # ropa local value
                                            c_double(roparegionlowervalue),     # ropa region lower value 
                                            c_double(roparegionuppervalue),     # ropa region upper value
                                            byref(coefficients),                # ropa coefficients
                                            byref(reactions),                   # ropa reactions indices
                                            c_int(numberofreactions))           # ropa number of reactions

		#  0-based
		# reaction-names 1-based
		reaction_names = []
		KineticMap = KineticMechanism(self.kineticFolder.decode("utf-8"))
		for i in reactions:
			reaction_names.append(KineticMap.returnReactionNameFromIndex(i))

		if (code == 0):
			if(self.verbose != False):
				print ('ROPA successfully executed')
			coefficients = [c for c in coefficients]
			reactions = [r for r in reactions]
			return coefficients, reactions, reaction_names
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
                                                    c_int(sensitivity),                # sensitivity type 0: local | 1: global | 2: region
                                                    c_int(ordering),                   # ordering type 0: peakvalues | 1: area | 2: absolutearea
                                                    c_int(normalization),              # normalization type 0: local | 1: maxvalue
                                                    c_double(sensitivitylocalvalue),       # sensitivity local value
                                                    c_double(sensitivityregionlowervalue), # sensitivity region lower value
                                                    c_double(sensitivityregionuppervalue), # sensitivity region upper value
                                                    byref(coefficients),                   # sensitivity coefficients
                                                    byref(reactions),                      # reactions indices
                                                    c_int(numberofreactions))              # sensitivity number of reactions
        
		#  0-based
		# reaction-names 1-based
		reaction_names = []
		KineticMap = KineticMechanism(self.kineticFolder.decode("utf-8"))
		for i in reactions:
			reaction_names.append(KineticMap.returnReactionNameFromIndex(i))

		if (code == 0):
			if(self.verbose != False):
				print('Sensitivity analysis succesfully executed')
			coefficients = [c for c in coefficients]
			reactions = [r for r in reactions]
			return coefficients, reactions, reaction_names
		else:
			raise ValueError('exit code != 0') # TODO
	
	def FluxAnalysis(self, specie: str, element: str, fluxanalysistype: str, 
						thickness: str, thicknesslogscale: bool, 
						labeltype: str, depth: int = 0, width: int = 0, 
						thresold: float = 0, ropalocalvalue: float = 0):
		specie = bytes(specie, 'utf-8')
		element = bytes(element, 'utf-8')
		
		if(fluxanalysistype == 'production'):
			flux = 1
		elif(fluxanalysistype == 'destruction'):
			flux = 0
		else:
			raise ValueError("The available type for the flux analysis are production | destruction")
		
		if(thickness == 'absolute'):
			thick = 0
		elif(thickness == 'relative'):
			thick = 1
		else:
			raise ValueError("The available type for the caluclation of the thicknsss are absolute | relative(%)")
	
		if(labeltype == 'absolute'):
			label = 0
		elif(labeltype == 'relative'):
			label = 1
		else:
			raise ValueError("The available type for the labeling are absolute | relative(%)")

		self.c_library.FluxAnalysis.argtypes = [c_char_p, # kinetic folder
												c_char_p, # output folder
												c_char_p, # specie
												c_char_p, # element
												c_int,    # flux analysis type
												c_double, # ropa local value
												c_int,    # thickness 0 absolute | 1 relative(%)
												c_bool,   # thickness log scale
												c_int,    # labeling type 0 absolute | 1 relative(%)
												c_int,    # depth
												c_int,    # width
												c_double, # thresold
												c_void_p, # indexes of the first name
												c_void_p, # indexes of the second name
												c_void_p, # computed thicknes value
												c_void_p, # computed label value
												c_void_p] # lenght of the vector to adjust (boring ctype stuff)

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
											c_int(flux),				 # flux analysis type
											c_double(ropalocalvalue),	 # ropa local value
											c_int(thick),				 # thickness 0 absolute | 1 relative(%)
											c_bool(thicknesslogscale),   # thickness log scale
											c_int(label),				 # labeling type 0 absolute | 1 relative(%)
											c_int(depth),				 # depth
											c_int(width),				 # width
											c_double(thresold),			 # thresold
											byref(indexFirstName),		 # indexes of the first name
											byref(indexSecondName),		 # indexes of the second name
											byref(computedThickness),	 # computed thicknes value
											byref(computedLabel),		 # computed label value
											byref(length))				 # lenght of the vector to adjust (boring ctype stuff)

		length = [l for l in length][0]
		indexFirstName = [i for i in indexFirstName][:length]
		indexSecondName = [i for i in indexSecondName][:length]
		computedThickness = [t for t in computedThickness][:length]
		computedLabel = [l for l in computedLabel][:length]

		self.firstNames = []
		self.secondNames = []
		KineticMap = KineticMechanism(self.kineticFolder.decode("utf-8"))

		for j in range(len(indexFirstName)):
			self.firstNames.append(KineticMap.returnSpecieNameFromIndex(indexFirstName[j]))
			self.secondNames.append(KineticMap.returnSpecieNameFromIndex(indexSecondName[j]))

		#print(self.firstNames)
		Graph = GrapWirter()
		Graph = Graph.CreateGraph(self.firstNames, self.secondNames, computedThickness, computedLabel)

		return Graph