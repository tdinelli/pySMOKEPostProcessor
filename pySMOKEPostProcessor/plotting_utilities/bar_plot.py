import re
import numpy as np
import matplotlib.pyplot as plt
# from .styles import *


def plot_multiple_bars(ax, data, colors=None, total_width=0.8,
                       single_width=1, y_names=None, legend=True):
    """Draws a bar plot with multiple bars per data point.

    Parameters
    ----------
    ax : matplotlib.pyplot.axis
        The axis we want to draw our plot on.

    data: dictionary
        A dictionary containing the data we want to plot. Keys are the names of
        the data, the items is a list of the values.

        Example:
        data = {
            "x":[1,2,3],
            "y":[1,2,3],
            "z":[1,2,3],
        }

    colors : array-like, optional
        A list of colors which are used for the bars. If None, the colors
        will be the standard matplotlib color cyle. (default: None)

    total_width : float, optional, default: 0.8
        The width of a bar group. 0.8 means that 80% of the x-axis is covered
        by bars and 20% will be spaces between the bars.

    single_width: float, optional, default: 1
        The relative width of a single bar within a group. 1 means the bars
        will touch eachother within a group, values less than 1 will make
        these bars thinner.

    legend: bool, optional, default: True
        If this is set to true, a legend will be added to the axis.
    """
    # Check if colors where provided, otherwhise use the default color cycle
    if colors is None:
        colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Number of bars per group
    n_bars = len(data)

    # The width of a single bar
    bar_width = total_width / n_bars

    # List containing handles for the drawn bars, used for the legend
    bars = []

    # Iterate over all data
    for i, (_, values) in enumerate(data.items()):
        # The offset in x direction of that bar
        x_offset = (i - n_bars / 2) * bar_width + bar_width / 2
        # Draw a bar for every value of that type
        for x, y in enumerate(values):

            # if y >= 0:
            # 	colori = 'red'
            # else:
            # 	colori = 'blue'

            # bar = ax.bar(x + x_offset, y, width=bar_width * single_width,
            # color=colors[i % len(colors)])
            bar = ax.barh(x + x_offset, y, height=bar_width * single_width,
                          color=colors[i % len(colors)])

            if i == 1:
                if (y < 0):
                    # , fontsize=18)
                    ax.text(0, x + x_offset, y_names[x], va='center')
                else:
                    # ,fontsize=18)
                    ax.text(0, x + x_offset,
                            y_names[x], va='center', ha='right')

        # Add a handle to the last drawn bar, which we'll need for the legend
        bars.append(bar[0])

    # Draw legend if we need
    if legend:
        ax.legend(bars, data.keys())

    xabs_max = abs(max(ax.get_xlim(), key=abs))
    ax.set_xlim(xmin=-xabs_max, xmax=xabs_max)
    ax.get_yaxis().set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.get_yaxis().set_ticks([])
    ax.invert_yaxis()

    return ax


def plot_bars(data: dict, ax=None, font: float = None):
    n_of_bars = len(data['coefficients'])
    if font is None:
        font =11-5*int(n_of_bars>20)

    index = np.arange(0, n_of_bars, 1)
    colors = []

    for i in data['coefficients']:
        if i >= 0:
            colors.append('red')
        else:
            colors.append('blue')

    if ax is None:
        fig = plt.figure()
        ax = plt.subplot()
    else:
        fig = ax.figure

    bar = ax.barh(index, data['coefficients'], color=colors)

    # fix rxn names for e.g., bin rxns
    pattern = re.compile(r'\d+\.\d+')
 
    for idx, i in enumerate(bar):
        x = i.get_width()
        y = i.get_y()+0.5*i.get_height()
        rxnname = pattern.sub(lambda x: "{:.2f}".format(float(x.group(0))), 
                              data['reaction_names'][idx])
        coefficient_value = "  (" + \
            str('{:6.4e}'.format(data['coefficients'][idx])) + ")"
        if (x < 0):
            ax.text(0,
                    y,
                    rxnname + coefficient_value,
                    va='center',
                    fontsize=font)
        else:
            ax.text(0,
                    y,
                    rxnname + coefficient_value,
                    va='center',
                    ha='right',
                    fontsize=font)

    xabs_max = abs(max(ax.get_xlim(), key=abs))
    ax.set_xlim(xmin=-xabs_max, xmax=xabs_max)

    # ax.get_yaxis().set_visible("off")
    # ax.axis("off")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.get_yaxis().set_ticks([])
    ax.invert_yaxis()

    return fig, ax


# [LG]  I think this might have been thought of with the plot_multiple_bars, but I found no example and I'm making this probably more general.
def plot_bars_multiSimulation(data_list: list, ax_list: list = None, cols: int = None, rows: int = None):
    is_nested = isinstance(data_list[0], (list, tuple))

    if is_nested:
        rows = len(data_list)
        cols = len(data_list[0])

        for row in data_list:
            if len(row) != cols:
                raise ValueError("data_list is non-rectangular")

        flat_data = [d for row in data_list for d in row]

    else:
        flat_data = data_list
        if rows is None and cols is None:
            rows = 1
            cols = len(flat_data)
        elif rows is None:
            rows = int(np.ceil(len(flat_data) / cols))
        elif cols is None:
            cols = int(np.ceil(len(flat_data) / rows))

    if ax_list is None:
        if rows * cols < len(flat_data):
            raise ValueError("Inconsistent number of points: grid too small for number of simulations")
        elif rows * cols > len(flat_data):
            raise ValueError("Inconsistent number of points: grid too big for number of simulations")

        fig, ax_list = plt.subplots(rows, cols)
        ax_list = np.atleast_1d(ax_list).flatten()
    else:
        fig = plt.gcf()
        ax_list = np.atleast_1d(ax_list).flatten()

    new_ax_list = []

    for data, ax in zip(flat_data, ax_list):
        fig, ax = plot_bars(data=data, ax=ax, font = 9)
        new_ax_list.append(ax)

    return fig, new_ax_list

