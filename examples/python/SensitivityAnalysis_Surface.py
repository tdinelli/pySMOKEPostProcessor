# Only for dev purposes
import os
import sys

import matplotlib.pyplot as plt
from pySMOKEPostProcessor.postprocessor import PostProcessor
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars

kineticFolder = os.path.join("..","data","Surface_Data","kinetics")
resultsFolder = os.path.join("..","data","Surface_Data","Output")

pp = PostProcessor(kineticFolder, resultsFolder)

target_species = "CH4"

# global_sensitivity = pp.SensitivityAnalysis_Surface(target=target_species,
#                                             sensitivity_type='global',
#                                             number_of_reactions=10,
#                                             ordering_type='peak-values',
#                                             normalization_type='local',
#                                             heterogeneous_sensitivity=False)
# fig_1, ax_1 = plot_bars(global_sensitivity)
# fig_1.suptitle(target_species, fontweight="bold")
# ax_1.set_title("Homogeneous Sensitivity")
# fig_1.set_size_inches(10, 6)
# fig_1.tight_layout()

global_sensitivity = pp.SensitivityAnalysis_Surface(target=target_species,
                                            sensitivity_type='global',
                                            number_of_reactions=20,
                                            ordering_type='peak-values',
                                            normalization_type='local',
                                            heterogeneous_sensitivity=True)
fig_2, ax_2 = plot_bars(global_sensitivity)
fig_2.suptitle(target_species, fontweight="bold")
ax_2.set_title("Heterogeneous Sensitivity")
fig_2.set_size_inches(16, 10)
fig_2.tight_layout()

plt.show()
