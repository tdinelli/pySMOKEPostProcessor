# Import main libraries
import numpy as np
import os
import matplotlib.pyplot as plt
import matplotlib
from mpl_toolkits.axes_grid1 import AxesGrid
#from .styles import *

def shiftedColorMap(cmap, start=0, midpoint=0.5, stop=1.0, name='shiftedcmap'):
    '''
    Function to offset the "center" of a colormap. Useful for
    data with a negative min and positive max and you want the
    middle of the colormap's dynamic range to be at zero.

    Input
    -----
      cmap : The matplotlib colormap to be altered
      start : Offset from lowest point in the colormap's range.
          Defaults to 0.0 (no lower offset). Should be between
          0.0 and `midpoint`.
      midpoint : The new center of the colormap. Defaults to 
          0.5 (no shift). Should be between 0.0 and 1.0. In
          general, this should be  1 - vmax / (vmax + abs(vmin))
          For example if your data range from -15.0 to +5.0 and
          you want the center of the colormap at 0.0, `midpoint`
          should be set to  1 - 5/(5 + 15)) or 0.75
      stop : Offset from highest point in the colormap's range.
          Defaults to 1.0 (no upper offset). Should be between
          `midpoint` and 1.0.
    '''
    cdict = {
        'red': [],
        'green': [],
        'blue': [],
        'alpha': []
    }

    # regular index to compute the colors
    reg_index = np.linspace(start, stop, 257)

    # shifted index to match the data
    shift_index = np.hstack([
        np.linspace(0.0, midpoint, 128, endpoint=False), 
        np.linspace(midpoint, 1.0, 129, endpoint=True)
    ])

    for ri, si in zip(reg_index, shift_index):
        r, g, b, a = cmap(ri)

        cdict['red'].append((si, r, r))
        cdict['green'].append((si, g, g))
        cdict['blue'].append((si, b, b))
        cdict['alpha'].append((si, a, a))

    newcmap = matplotlib.colors.LinearSegmentedColormap(name, cdict)
    plt.register_cmap(cmap=newcmap)

    return newcmap

def plot_heatmap(sort_df, weigheach = True):
	"""
	heat maps of x: df.columns, y: df.index 
	"""
	# generate the figure
	fig, axes = plt.subplots(figsize = [len(sort_df.columns), len(sort_df.index)])
	# valmax = max([np.min(sort_df.values), np.max(sort_df.values)])
	if weigheach:
		image = axes.imshow(sort_df.values, 
		    aspect='auto', cmap='RdBu_r',
			vmin=-1, 
			vmax=1)  # coolwarm, RdBu, seismic, bwr
	else:
		orig_cmap = matplotlib.cm.RdBu_r
		
		vmin = sort_df.min(numeric_only=True).min() 
		vmax = sort_df.max(numeric_only=True).max()
		midpoint = 1 - vmax/(vmax + abs(vmin))
		
		shifted_cmap = shiftedColorMap(orig_cmap, midpoint=midpoint, name='shifted')
		image = axes.imshow(sort_df.values,
		    interpolation='none', 
			cmap=shifted_cmap)  # coolwarm, RdBu, seismic, bwr
    
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