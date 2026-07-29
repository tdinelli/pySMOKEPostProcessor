import os
import matplotlib.pyplot as plt
# from pySMOKEPostProcessor.plotting_utilities.bar_plot import plot_bars
# from pySMOKEPostProcessor import plot_heatmap
# from pySMOKEPostProcessor import script_utils
from pySMOKEPostProcessor.surfacereactions_utilities.deposition_plot import CumulativeDeposition,CumulativeSootProduction

kineticFolder = os.path.join("..","data","Surface_Data","kinetics")
# kineticFile = os.path.join(kineticFolder,"kinetics.surface.xml")
resultsFolder = os.path.join("..","data","Surface_Data","Output")

surface_classes = os.path.join('..', 'data', 'Surface_Data', 'surf_rxn_class.txt')
gas_classes = os.path.join('..', 'data', 'ReactionClasses', 'rxn_class_groups.txt')
sortlists = [['reactiontype']]  # Ask Luna why this is a list of lists  # classtype, speciestype, subclass, bimoltype, reactiontype

lump_steps = 4  # To make it faster (less resolution)

Bulk = CumulativeDeposition(    kineticFolder=kineticFolder, outputFolder=resultsFolder, class_group_file=surface_classes,  sort_type=sortlists, area=200./1E4, allCarbon=True)
Soot = CumulativeSootProduction(kineticFolder=kineticFolder, outputFolder=resultsFolder, class_group_file=gas_classes,      sort_type=sortlists, volume=100./1E4)

fig,ax = plt.subplots(2,1,figsize=(10.5,12.), sharex=True)

fig,ax[0] = Bulk.plotCumulativeDeposition(lump_steps=lump_steps,units='mass',fig=fig,ax=ax[0])
fig,ax[1] = Soot.plotSootProduction(      lump_steps=lump_steps,units='mass',fig=fig,ax=ax[1])

ymax = max(ax[0].get_ylim()[1], ax[1].get_ylim()[1])
ax[0].set_ylim(top=ymax*1.1)
ax[1].invert_yaxis()
ax[1].set_ylim(bottom=ymax*1.1)

fig.tight_layout()
#fig.savefig("Deposition_Soot.png", dpi=300)
plt.show()
