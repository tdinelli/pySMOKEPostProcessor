# Only for dev purposes
import os
# import sys
#

from pySMOKEPostProcessor.postprocessor import PostProcessor
import matplotlib.pyplot as plt
# from postprocessor import PostProcessor
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars

kineticFolder = os.path.join("..","data","Surface_Data","kinetics")
resultsFolder = os.path.join("..","data","Surface_Data","Output")

pp = PostProcessor(kineticFolder, resultsFolder)

global_ropa_homo = pp.RateOfProductionAnalysis_Surface(species='CH4',
                                          ropa_type='global',
                                          number_of_reactions=10,
                                          heterogeneous_reactions=False)

result_homo = {
    "coefficients": global_ropa_homo["coefficients"],
    "reaction_names": global_ropa_homo["reaction_names"],
    "reaction_indices": global_ropa_homo["reaction_indices"]
}

fig_1, ax_1 = plot_bars(result_homo)
fig_1.suptitle("Homogeneous ROPA")
fig_1.tight_layout()

global_ropa_het = pp.RateOfProductionAnalysis_Surface(species='CH4',
                                          ropa_type='global',
                                          number_of_reactions=10,
                                          heterogeneous_reactions=True)

result_het = {
    "coefficients": global_ropa_het["coefficients"],
    "reaction_names": global_ropa_het["reaction_names"],
    "reaction_indices": global_ropa_het["reaction_indices"]
}

fig_2, ax_2 = plot_bars(result_het)
fig_2.suptitle("Heterogeneous ROPA")
fig_2.tight_layout()

# local_ropa = pp.RateOfProductionAnalysis(species='H2',
#                                          ropa_type='local',
#                                          local_value=0.001,
#                                          number_of_reactions=10)

# fig_2, ax_2 = plot_bars(local_ropa)

# region_ropa = pp.RateOfProductionAnalysis(species='H2',
#                                           ropa_type='region',
#                                           lower_value=0.0005,
#                                           upper_value=0.0009,
#                                           number_of_reactions=15)

# fig_3, ax_3 = plot_bars(region_ropa)

plt.show()
