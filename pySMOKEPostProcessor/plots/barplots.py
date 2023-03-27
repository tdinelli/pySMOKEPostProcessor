import numpy as np
import os
import matplotlib.pyplot as plt

def plot_bars(df, type: str, title: str = ''):
    """Plots ROPA/SENS as bar plots

    Args:
        df (pandas dataframe): columns 'ROPA-Coeff' or 'SENS-Coeff' and 'Reaction Name'
        type (str): ROPA or SENS
        title (str, optional): plot title
    """
    
    if type in ['ROPA', 'SENS']:
        col = type + '-Coeff'
    else:
        raise ValueError('type must be ROPA or SENS')
    
    fig = plt.figure(figsize=(15, 12))
    ax = plt.subplot()
    
    if len(title) > 0:
        ax.set_title(title, fontsize = 20)
    
    bar = ax.barh(df.index, 
                df[col], 
                color = (df[col] >= 0.).map({True:'red', False:'blue'}))

    for idx, i in enumerate(bar):
        x = i.get_width()
        y = i.get_y()+0.5*i.get_height()
        if(x<0):
            ax.text(0, y, 
                df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df[col][idx])) + ")", 
                va='center', fontsize=14)
        else:
            ax.text(0,
                    y, 
                    df['Reaction Name'][idx] + "  (" + str('{:6.4f}'.format(df[col][idx])) + ")", 
                    va='center',
                    ha='right',
                    fontsize=14) 

    ax.set_yticks(np.arange(0, 10, 1))
    ax.set_yticklabels([])
    ax.set_xticklabels([])
    ax.axis("off")
    ax.invert_yaxis()
    
    return fig