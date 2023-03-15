from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
import pySMOKEPostProcessor as pp
from IPython.display import Image, display
import networkx as nx

# Only for dev purposes
import os.path
if os.path.isdir("/Users/tdinelli/"):
	pp.load("/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/build/libpySMOKEPostProcessor.dylib")

kineticFolder = os.path.join("examples", "data", "ROPA-01", "kinetics")
resultsFolder = os.path.join("examples", "data", "ROPA-01", "Output")
kineticFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/kinetics"
resultsFolder = "/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/examples/data/ROPA-01/Output"
G = pp.FluxAnalysis(kinetic_folder=kineticFolder, 
                    output_folder=resultsFolder,
					species = "H2", 
                    element = "H", 
                    flux_analysis_type = "destruction", 
                    thickness = "relative", 
                    thickness_log_scale = True, 
                    label_type = "relative", 
                    depth = 2, 
                    width = 5, 
                    threshold = 0.01, 
                    local_value = 0.003258)

P = nx.drawing.nx_pydot.to_pydot(G)
img = Image(P.create_png())  
display(img)