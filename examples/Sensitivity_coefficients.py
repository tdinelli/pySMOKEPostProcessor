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

kineticFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/Sensitivity-01/kinetics"
resultsFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/Sensitivity-01/Output-01"

time, sensitivity_coefficient = pp.SensitivityCoefficients(kinetic_folder=kineticFolder,
                                                        output_folder=resultsFolder,
	                                                    target='O2', 
                                                        reaction_name='O2+H=O+OH', 
                                                        normalization_type='max-value')

plt.plot(time, sensitivity_coefficient, label = 'R1: O2+H=O+OH')
plt.xlabel('time [s]', fontsize=20)
plt.ylabel('$S^{O_{2}}_{R_{1}}$', fontsize=20)
plt.legend()
plt.grid()
plt.show()