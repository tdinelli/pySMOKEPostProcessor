import numpy as np
import matplotlib.pyplot as plt
from .styles import *

# def bar_plot(ax, data, colors=None, total_width=0.8, single_width=1, y_names=None, legend=True):
# 	"""Draws a bar plot with multiple bars per data point.
#
# 	Parameters
# 	----------
# 	ax : matplotlib.pyplot.axis
# 		The axis we want to draw our plot on.
#
# 	data: dictionary
# 		A dictionary containing the data we want to plot. Keys are the names of the
# 		data, the items is a list of the values.
#
# 		Example:
# 		data = {
# 			"x":[1,2,3],
# 			"y":[1,2,3],
# 			"z":[1,2,3],
# 		}
#
# 	colors : array-like, optional
# 		A list of colors which are used for the bars. If None, the colors
# 		will be the standard matplotlib color cyle. (default: None)
#
# 	total_width : float, optional, default: 0.8
# 		The width of a bar group. 0.8 means that 80% of the x-axis is covered
# 		by bars and 20% will be spaces between the bars.
#
# 	single_width: float, optional, default: 1
# 		The relative width of a single bar within a group. 1 means the bars
# 		will touch eachother within a group, values less than 1 will make
# 		these bars thinner.
#
# 	legend: bool, optional, default: True
# 		If this is set to true, a legend will be added to the axis.
# 	"""
# 	# Check if colors where provided, otherwhise use the default color cycle
# 	if colors is None:
# 		colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
#
# 	# Number of bars per group
# 	n_bars = len(data)
#
# 	# The width of a single bar
# 	bar_width = total_width / n_bars
#
# 	# List containing handles for the drawn bars, used for the legend
# 	bars = []
#
# 	hatch_list = ['////', '....', 'ooo']
# 	# Iterate over all data
# 	for i, (name, values) in enumerate(data.items()):
# 		# The offset in x direction of that bar
# 		x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
# 		# Draw a bar for every value of that type
# 		for x, y in enumerate(values):
#
# 			#if y >= 0:
# 			#	colori = 'red'
# 			#else:
# 			#	colori = 'blue'
#
# 			# bar = ax.bar(x + x_offset, y, width=bar_width * single_width, color=colors[i % len(colors)])
# 			bar = ax.barh(x + x_offset, y, height=bar_width * single_width, color=colors[i % len(colors)])
#
# 			if i == 1:
# 				if(y<0):
# 					ax.text(0, x + x_offset, y_names[x], va='center')#, fontsize=18)
# 				else:
# 					ax.text(0, x + x_offset, y_names[x], va='center', ha='right')#,fontsize=18)  
#
# 		# Add a handle to the last drawn bar, which we'll need for the legend
# 		bars.append(bar[0])
#
# 	# Draw legend if we need
# 	if legend:


def plot_bars(data: dict):
    index = np.arange(0, len(data['coefficients']), 1)
    colors = []

    for i in data['coefficients']:
        if i >= 0:
            colors.append('red')
        else:
            colors.append('blue')

    fig = plt.figure()
    ax = plt.subplot()
    bar = ax.barh(index, data['coefficients'], color=colors)

    for idx, i in enumerate(bar):
        x = i.get_width()
        y = i.get_y()+0.5*i.get_height()
        coefficient_value = "  (" + str('{:6.4e}'.format(data['coefficients'][idx])) + ")"
        if (x < 0):
            ax.text(0,
                    y,
                    data['reaction_names'][idx] + coefficient_value,
                    va='center',
                    fontsize=11)
        else:
            ax.text(0,
                    y,
                    data['reaction_names'][idx] + coefficient_value,
                    va='center',
                    ha='right',
                    fontsize=11)

    xabs_max = abs(max(ax.get_xlim(), key=abs))
    ax.set_xlim(xmin=-xabs_max, xmax=xabs_max)

    # ax.set_yticklabels([])
    # ax.set_xticklabels([])
    # ax.get_yaxis().set_visible("off")
    # ax.axis("off")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    # ax.get_xaxis().set_ticks([])
    ax.get_yaxis().set_ticks([])
    ax.invert_yaxis()

    return fig, ax
