from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pySMOKEPostProcessor as pp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Only for dev purposes
import os.path
if os.path.isdir("/Users/tdinelli/"):
	pp.load("/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib")

kineticFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/kinetics"
resultsFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/Output"

abscissae, reaction_rate = pp.GetReactionRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            reaction_name = 'O2+H=O+OH')

plt.plot(abscissae, reaction_rate, 'r')
plt.xlabel('Temperature [K]', fontsize=15)
plt.ylabel('Reaction Rate [kmol/m3/s]', fontsize=15)
plt.grid()
plt.show()

abscissae, reaction_rate_1 = pp.GetReactionRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            reaction_name = 'O2+H=O+OH')
abscissae, reaction_rate_2 = pp.GetReactionRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            reaction_name = 'H2+O=H+OH')
abscissae, reaction_rate_3 = pp.GetReactionRates(kinetic_folder = kineticFolder,
					    					output_folder = resultsFolder,
											abscissae_name = 'temperature', 
                                            reaction_name = 'O2+H(+M)=HO2(+M)')

plt.plot(abscissae, reaction_rate_1, 'r', label = 'O2+H=O+OH')
plt.plot(abscissae, reaction_rate_2, 'b', label = 'H2+O=H+OH')
plt.plot(abscissae, reaction_rate_3, 'g', label = 'O2+H(+M)=HO2(+M)')
plt.xlabel('Temperature [K]', fontsize=15)
plt.ylabel('Reaction Rate [kmol/m3/s]', fontsize=15)
plt.legend()
plt.grid()
plt.show()