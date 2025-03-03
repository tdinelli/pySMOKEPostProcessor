import re
import matplotlib.pyplot as plt
# from .styles import *


def plot_areas(data_df, xlabel = 'x axis', ylabel = 'y axis', title = '',
               fontsize = '8', loc = 'upper right', plotlines = False):
    """Draws a plot with shaded areas
    Parameters
    ----------
    data_df: datafame with data
    index: x axis
    columns: names   
    """
    linestyles = ['-', '--', '-.', ':']*(round(len(data_df.columns)/4)+1)
    fig, ax = plt.subplots(nrows=1, ncols=1)
    for i, item in enumerate(data_df.columns):
        if plotlines:
            ax.plot(data_df.index, data_df[item].values, linestyle =linestyles[i])
        else:
            ax.stackplot(data_df.index, data_df[item].values, edgecolor = 'black', alpha = 0.5)
    # edit legend (fix for bins)
    leg = []
    pattern = re.compile(r'\d+\.\d+')
    for rxnname in data_df.columns:
        leg.append(pattern.sub(lambda x: "{:.5f}".format(float(x.group(0))), rxnname))
        
    ax.legend(leg, fontsize = fontsize, loc = loc)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax.set_title(title)
    fig.tight_layout()

    return fig, ax

