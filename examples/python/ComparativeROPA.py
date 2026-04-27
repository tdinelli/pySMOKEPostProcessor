import os
import numpy as np
import matplotlib.pyplot as plt
from pySMOKEPostProcessor.postprocessor import PostProcessor
from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars_multiSimulation

# TODO the paths are to be fixed Do we have two similar examples which might be compared? 
# I might load two different mechanisms for the same simulation for this.

kin_root = "/home/lgiardini/Mechanisms"
kin_list = ["Nobili_Gas", "GasC3", "WangMech"]

case_info = [
    ["Bedarev", "Case10"],
    ["Hidaka",  "Case10"]
]
labels = ["Bedarev","Hidaka"]

# ROPA setup
target_species = "C2H4"
num_rxns = 8
ropa_type = "global"

ppList = []

for j, case in enumerate(case_info):
    row = []

    for i, kin in enumerate(kin_list):

        # kinetic folder
        kineticFolder = os.path.join(kin_root, kin)

        # output folder
        if len(case) == 1:
            outputFolder = os.path.join(case[0],kin)
        elif len(case) == 2:
            outputFolder = os.path.join(case[0],kin,case[1])

        pp = PostProcessor(kineticFolder, outputFolder)
        row.append(pp)

    ppList.append(row)

ropa = []
for j, row in enumerate(ppList):
    ropa_row = []

    for i, pp in enumerate(row):
        r = pp.RateOfProductionAnalysis(
            species=target_species,
            ropa_type=ropa_type,
            number_of_reactions=num_rxns,
        )
        ropa_row.append(r)

    ropa.append(ropa_row)

fig, ax_list = plot_bars_multiSimulation( data_list=ropa )
# fig.subplots_adjust(left=-0.1)

rows = len(case_info)
cols = len(kin_list)
base_w = 5
base_h = 4

fig.set_size_inches(cols * base_w, rows * base_h)
ax_array = np.array(ax_list).reshape(rows, cols)
for j, kin in enumerate(kin_list):
    ax_array[0, j].set_title(kin,fontweight='bold',fontsize=20)

for i, case in enumerate(case_info):
    # if len(case) == 2:
    #     label = case[1]
    # else:
    #     label = case[0]

    label = labels[i]
    ax_array[i, 0].set_ylabel(label,fontweight='bold',fontsize=20)

for i in range(rows):
    for j in range(cols):
        ax_array[i, j].set_xticklabels([])
        if j > 0:
            ax_array[i, j].set_yticklabels([])

plt.show()