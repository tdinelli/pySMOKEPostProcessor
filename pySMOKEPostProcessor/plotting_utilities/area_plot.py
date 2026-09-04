import matplotlib.pyplot as plt
# from .styles import *

def plot_class_distribution(data_df, xlabel='coordinate', ylabel='element fraction', title='',
                            colors=None, fontsize=8, loc='upper right', edgecolor='k',
                            linewidth=0.4, alpha=1.0, reverse_legend=True):
    """Stacked-area plot of a per-class distribution along the independent variable.

    One filled band per class, one colour per class. ``stackplot`` uses
    ``baseline='zero'``, so band k sits on top of the sum of bands 0..k-1; when
    ``data_df`` rows already sum to 1 (the normalised elemental distribution) the
    bands fill the axes from 0 to 1. This is the primitive a future
    surface/deposition-style variant is expected to build on.

    Parameters
    ----------
    data_df : DataFrame
        index = independent variable (time, space, ...), one column per class,
        values already normalised row-wise if a 0-100% view is wanted.
    colors : list, optional
        one colour per kept column; defaults to seaborn "muted" when seaborn is
        available, otherwise the matplotlib tab20 cycle.
    reverse_legend : bool
        stackplot draws the first column at the bottom and the last at the top;
        with reverse_legend=True (default) the legend is ordered top band first,
        so it reads in the same order as the visible stack.
    """
    columns = [c for c in data_df.columns if data_df[c].abs().to_numpy().sum() > 0]

    if colors is None:
        try:
            import seaborn as sns
            colors = list(sns.color_palette('muted', len(columns)))
        except ImportError:
            cmap = plt.get_cmap('tab20')
            colors = [cmap(i % cmap.N) for i in range(len(columns))]

    fig, ax = plt.subplots(nrows=1, ncols=1)
    ax.stackplot(
        data_df.index,
        *[data_df[c].to_numpy() for c in columns],
        labels=columns,
        colors=colors[:len(columns)],
        baseline='zero',
        edgecolor=edgecolor,
        linewidth=linewidth,
        alpha=alpha,
    )
    ax.set_xlim(data_df.index.min(), data_df.index.max())
    ax.set_ylim(0, 1)

    handles, labels = ax.get_legend_handles_labels()
    if reverse_legend:
        handles, labels = handles[::-1], labels[::-1]
    ax.legend(handles, labels, fontsize=fontsize, loc=loc)

    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.tight_layout()

    return fig, ax
