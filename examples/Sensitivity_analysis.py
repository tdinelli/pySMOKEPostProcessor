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

specie = "NO"

coefficients, indices, names = pp.SensitivityAnalysis(kinetic_folder=kineticFolder,
                                                    output_folder=resultsFolder,
													target=specie, 
													sensitivity_type='global', 
													number_of_reactions=20,
													ordering_type="peak-values",
													normalization_type='local')

dic = {'Sensitivity-Coeff': coefficients,'Indices-0based': indices, 'Reaction Name': names}
df = pd.DataFrame(dic)

fig = plt.figure(figsize=(18, 12))
ax = plt.subplot()
ax.set_title("$NO$ Global Sensitivity Analysis\n ", fontsize=28)
bar = ax.barh(df.index, df['Sensitivity-Coeff'], color = (df['Sensitivity-Coeff'] >=0.).map({True:'red', False:'blue'}))
for idx, i in enumerate(bar):
    x = i.get_width()
    y = i.get_y()+0.5*i.get_height()
    if(x<0):
        ax.text(0, y, 
            df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df["Sensitivity-Coeff"][idx])) + ")", 
            va='center', fontsize=18)
    else:
        ax.text(0, y, 
            df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df["Sensitivity-Coeff"][idx])) + ")", 
            va='center', ha='right',fontsize=18)  

ax.set_yticks(np.arange(0, 10, 1))
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.axis("off")
ax.invert_yaxis()
plt.show()