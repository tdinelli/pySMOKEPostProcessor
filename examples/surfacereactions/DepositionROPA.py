import os
import matplotlib.pyplot as plt
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars
from pySMOKEPostProcessor import plot_heatmap
from pySMOKEPostProcessor import script_utils
from pySMOKEPostProcessor.surfacereactions_utilities.deposition_plot import CumulativeDeposition

kineticFolder = os.path.join("..","data","Surface_Data","kinetics")
# kineticFile = os.path.join(kineticFolder,"kinetics.surface.xml")
resultsFolder = os.path.join("..","data","Surface_Data","Output")

class_groups_file = os.path.join('..', 'data', 'Surface_Data', 'surf_rxn_class.txt')
sortlists = [['reactiontype']]  # Ask Luna why this is a list of lists

obj = CumulativeDeposition(kineticFolder=kineticFolder, outputFolder=resultsFolder, class_group_file=class_groups_file)

obj.setClassification(sort_type=sortlists)
obj.plotCumulativeDeposition(lump_steps=1)

plt.show()
