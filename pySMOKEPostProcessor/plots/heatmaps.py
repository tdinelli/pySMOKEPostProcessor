# Import main libraries
import numpy as np
import os
import matplotlib.pyplot as plt

# TODO
# Luna questo prevede la possibilità di usare fogli di stile 
# sarebbe meglio di no
plt.style.use('default')



def plot_heatmap(sort_df, savepath):
    """
    heat maps of x: df.columns, y: df.index 
    """
    # generate the figure
    fig, axes = plt.subplots(
        figsize=[len(sort_df.columns), len(sort_df.index)])
    # valmax = max([np.min(sort_df.values), np.max(sort_df.values)])
    image = axes.imshow(sort_df.values, aspect='auto', cmap='RdBu_r',
    #)
                        vmin=-1, vmax=1)  # coolwarm, RdBu, seismic, bwr
    axes.set_yticks(np.arange(0, len(sort_df.index)))    
    axes.set_xticks(np.arange(0, len(sort_df.columns)))
    size_for_lbl = 'xx-large'*(len(sort_df.index) > 3) + 'medium'*(len(sort_df.index) <= 3)

    axes.set_yticklabels([idx.split('flux_')[1] for idx in sort_df.index], fontsize=size_for_lbl)
    axes.set_xticklabels(sort_df.columns, rotation=90, fontsize=size_for_lbl)
    #image.figure.axes[1].tick_params(axis="y", labelsize=size_for_lbl) # colorbar
    plt.colorbar(image)
    
    

    fig.tight_layout()
    # save the figure

    if os.path.isfile(savepath):
        os.remove(savepath)
    fig.savefig(savepath, dpi=200)

    plt.close()

def show_heatmap(sort_df):
    """
    heat maps of x: df.columns, y: df.index 
    """
    # generate the figure
    fig, axes = plt.subplots(figsize=[len(sort_df.columns), len(sort_df.index)])

    image = axes.imshow(sort_df.values, 
                        aspect='auto', 
                        cmap='RdBu_r',
                        vmin=-1, vmax=1)
                        
    axes.set_yticks(np.arange(0, len(sort_df.index)))    
    axes.set_xticks(np.arange(0, len(sort_df.columns)))
    size_for_lbl = 'xx-large'*(len(sort_df.index) > 3) + 'medium'*(len(sort_df.index) <= 3)

    axes.set_yticklabels([idx.split('flux_')[1] for idx in sort_df.index], fontsize=size_for_lbl)
    axes.set_xticklabels(sort_df.columns, rotation=90, fontsize=size_for_lbl)
    plt.colorbar(image)

    fig.tight_layout()

    plt.show()
