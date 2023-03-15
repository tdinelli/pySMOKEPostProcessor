from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pySMOKEPostProcessor as pp
import matplotlib.pyplot as plt

# Only for dev purposes
import os.path
if os.path.isdir("/Users/tdinelli/"):
	pp.load("/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib")

kineticFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/kinetics"
resultsFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/Output"

abscissae, formation_rates = pp.GetFormationRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            species = 'H2',
                                            units = 'mole',
                                            formation_rate_type = 'destruction')

plt.plot(abscissae, formation_rates, 'r', label = 'H2')
plt.xlabel('Temperature [K]', fontsize=15)
plt.ylabel('Formation Rate [kmol/m3/s]', fontsize=15)
plt.legend()
plt.grid()
plt.show()

abscissae, formation_rate_H2 = pp.GetFormationRates(kinetic_folder = kineticFolder,
					    						output_folder = resultsFolder,
												abscissae_name = 'temperature', 
                                                species = 'H2',
                                                units = 'mass',
                                                formation_rate_type = 'net')

abscissae, formation_rate_H2O = pp.GetFormationRates(kinetic_folder = kineticFolder,
					    						output_folder = resultsFolder,
												abscissae_name = 'temperature', 
                                                species = 'H2O',
                                                units = 'mass',
                                            	formation_rate_type = 'net')

plt.plot(abscissae, formation_rate_H2, 'r', label = 'H2')
plt.plot(abscissae, formation_rate_H2O, 'b', label = 'H2O')
plt.xlabel('Temperature [K]', fontsize=15)
plt.ylabel('Formation Rate [kg/m3/s]', fontsize=15)
plt.legend()
plt.grid()
plt.show()

abscissae, char_time_CO2 = pp.GetFormationRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            species = 'CO2',
                                            units = 'mole',
                                            formation_rate_type = 'characteristic-time')

plt.plot(abscissae, char_time_CO2, 'r', label = 'CO2')
plt.xlabel('Temperature [K]', fontsize=15)
plt.ylabel('Characteristic time [s]', fontsize=15)
plt.yscale('log')
plt.legend()
plt.grid()
plt.show()
