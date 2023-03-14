from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pySMOKEPostProcessor as pp
import pandas as pd
import plotly.graph_objects as go
import numpy as np

# Only for dev purposes
import os.path
if os.path.isdir("/Users/tdinelli/"):
    pp.load("/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib")

kineticFolder = path.join("data", "ROPA-01", "kinetics")
resultsFolder = path.join("data", "ROPA-01", "Output")

coefficients, indices, names = pp.RateOfProductionAnalysis(kinetic_folder=kineticFolder, 
                                        output_folder=resultsFolder,
                                        species='H2',
                                        ropa_type='global')

dic = {'ROPA-Coeff': coefficients,'Indices-0based': indices, 'Reaction Name': names}
df = pd.DataFrame(dic)
df["Color"] = np.where(df["ROPA-Coeff"]<0, 'blue', 'red')

fig = go.Figure(go.Bar(x=df["ROPA-Coeff"], 
                       orientation='h', 
                       marker=dict(color=df['Color'],
                                   line=dict(color='white', width=1.2)
                                   )
                    )
                )

fig.update_layout(yaxis=dict(autorange="reversed"))
fig.show()