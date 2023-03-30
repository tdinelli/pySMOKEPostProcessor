# Import main libraries
import numpy as np
import os
import matplotlib.pyplot as plt
#from .styles import *

def plot_heatmap(sort_df):
	"""
	heat maps of x: df.columns, y: df.index 
	"""
	# generate the figure
	fig, axes = plt.subplots(figsize = [len(sort_df.columns), len(sort_df.index)])
	# valmax = max([np.min(sort_df.values), np.max(sort_df.values)])

	image = axes.imshow(sort_df.values, aspect='auto', cmap='RdBu_r',
                    	vmin=-1, vmax=1)  # coolwarm, RdBu, seismic, bwr
    
	axes.set_yticks(np.arange(0, len(sort_df.index)))    
	axes.set_xticks(np.arange(0, len(sort_df.columns)))
    
	size_for_lbl = 'xx-large'*(len(sort_df.index) > 3) + 'medium'*(len(sort_df.index) <= 3)

	axes.set_yticklabels([idx.split('flux_')[1] for idx in sort_df.index], fontsize=size_for_lbl)
	axes.set_xticklabels(sort_df.columns, rotation=90, fontsize=size_for_lbl)
    
    
	plt.colorbar(image)
	fig.tight_layout()
    
	return fig

def save_fig(fig, plt_fld, sortlist, simul_name):          
    
	if len(sortlist) > 1:
		criteria_str = '-'.join(sortlist)
	else:
		criteria_str = sortlist[0]
    
	savepath = os.path.join(plt_fld, '{}_{}.png'.format(simul_name, criteria_str))  
    
	# save the figure
	if os.path.isfile(savepath):
		os.remove(savepath)
    
	fig.savefig(savepath, dpi=200)