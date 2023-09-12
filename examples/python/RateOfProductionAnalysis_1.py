# Only for dev purposes
import os
import sys

if os.path.isdir("/home/chimica2/tdinelli"):
    sys.path.append('/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/pySMOKEPostProcessor')
elif os.path.isdir("/Users/tdinelli"):
    sys.path.append('/Users/tdinelli/Documents/GitHub/pySMOKEPostProcessor/pySMOKEPostProcessor')

import matplotlib.pyplot as plt
from postprocessor import PostProcessor
from plotting_utilities.bar_plot import plot_bars

kineticFolder = os.path.join("..", "data", "ROPA-01", "kinetics")
resultsFolder = os.path.join("..", "data", "ROPA-01", "Output")

pp = PostProcessor(kineticFolder, resultsFolder)

global_ropa = pp.RateOfProductionAnalysis(species='H2',
                                          ropa_type='global',
                                          number_of_reactions=10)

fig_1, ax_1 = plot_bars(global_ropa)

local_ropa = pp.RateOfProductionAnalysis(species='H2',
                                         ropa_type='local',
                                         local_value=0.001,
                                         number_of_reactions=10)

fig_2, ax_2 = plot_bars(local_ropa)

region_ropa = pp.RateOfProductionAnalysis(species='H2',
                                          ropa_type='region',
                                          lower_value=0.0005,
                                          upper_value=0.0009,
                                          number_of_reactions=15)

fig_3, ax_3 = plot_bars(region_ropa)

plt.show()
