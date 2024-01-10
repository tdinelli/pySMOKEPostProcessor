import sys
from pySMOKEPostProcessor import PostProcessor
from IPython.display import Image, display
import networkx as nx
import os

kineticFolder = os.path.join("..", "data", "ROPA-01", "kinetics")
resultsFolder = os.path.join("..", "data", "ROPA-01", "Output")

pp = PostProcessor(kineticFolder, resultsFolder)

G = pp.FluxAnalysis(species = "H2", 
                    element = "H", 
                    flux_analysis_type = "destruction", 
                    thickness = "relative", 
                    thickness_log_scale = True, 
                    label_type = "relative", 
                    depth = 1, 
                    width = 3, 
                    threshold = 0.01, 
                    local_value = 0.001)

display(G)
