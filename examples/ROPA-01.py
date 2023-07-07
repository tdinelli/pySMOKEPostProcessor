import pySMOKEPostProcessor as pp
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

kineticFolder = os.path.join("data", "ROPA-01", "kinetics")
resultsFolder = os.path.join("data", "ROPA-01", "Output")

pp.GetSimulationsBoundary(kineticFolder, resultsFolder)
pp.GetSimulationINFO(kineticFolder, resultsFolder)

coefficients, indices, names = pp.RateOfProductionAnalysis(kinetic_folder=kineticFolder, 
	output_folder=resultsFolder,
	species='H2',
	ropa_type='local', 
	local_value=0.0003,
	number_of_reactions=20)

dic = {'ROPA-Coeff': coefficients,'Indices-0based': indices, 'Reaction Name': names}
df = pd.DataFrame(dic)

fig = plt.figure(figsize=(12, 6))
ax = plt.subplot()
ax.set_title("$H_{2}$ Global Rate Of Production Analysis", fontsize=28)
bar = ax.barh(df.index, df['ROPA-Coeff'], color = (df['ROPA-Coeff'] >= 0.).map({True:'red', False:'blue'}))

for idx, i in enumerate(bar):
	x = i.get_width()
	y = i.get_y()+0.5*i.get_height()
	if(x<0):
		ax.text(0,
			y, 
			df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df["ROPA-Coeff"][idx])) + ")", 
			va='center', fontsize=18)
	else:
		ax.text(0,
			y, 
			df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df["ROPA-Coeff"][idx])) + ")", 
			va='center',
			ha='right',
			fontsize=18) 

ax.margins(x=0.9, y=0)
#ax.margins(x=0)
#ax.set_aspect('equal', 'box')
#ax.set_aspect('equal')
#ax.set_yticks(np.arange(0, 10, 1))
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.axis("off")
ax.invert_yaxis()
#fig.tight_layout()
plt.show()
