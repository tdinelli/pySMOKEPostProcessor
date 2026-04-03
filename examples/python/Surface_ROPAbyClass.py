# Only for dev purposes
import os
# import sys
#

from pySMOKEPostProcessor.postprocessor import PostProcessor
import matplotlib.pyplot as plt
# from postprocessor import PostProcessor
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars
from pySMOKEPostProcessor.maps.KineticMap import KineticMapSurface

kineticFolder = os.path.join("..","data","Surface_Data","kinetics")
kineticFile = os.path.join(kineticFolder,"kinetics.surface.xml")
resultsFolder = os.path.join("..","data","Surface_Data","Output")

pp = PostProcessor(kineticFolder, resultsFolder)


kms = KineticMapSurface(kineticFolder)
kms.ParseSurfaceKinetics(kineticFile)
kms.Classes()

print(kms.classes)