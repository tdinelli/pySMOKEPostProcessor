# Only for dev purposes
import os
import sys

import matplotlib.pyplot as plt
from pySMOKEPostProcessor.postprocessor import PostProcessor
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars

kineticFolder = os.path.join("..", "data", "Sensitivity-01", "kinetics")
resultsFolder = os.path.join("..", "data", "Sensitivity-01", "Output-01")

pp = PostProcessor(kineticFolder, resultsFolder)

global_sensitivity = pp.SensitivityAnalysis(target='NO',
                                            sensitivity_type='global',
                                            number_of_reactions=20,
                                            ordering_type='peak-values',
                                            normalization_type='local')

fig_1, ax_1 = plot_bars(global_sensitivity)

plt.show()
