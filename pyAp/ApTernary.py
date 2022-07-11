"""
Weiran Li & Yishen Zhang

2022-02-20, v0.2

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import matplotlib.pyplot as plt, math, numpy as np

fontsize = 14

def ternary(ax):
    """
    Function for apatite ternary plot on an axis ("ax" as input).

    The figure where the axis is located needs to be defined outside of this function.

    """
    # set axis aspect
    ax.set_aspect('equal')
    ax.axis('off')

    # plot ternary boundaries
    ax.plot([0,100],[0,0],'k-')
    ax.plot([0,50],[0,50*math.sqrt(3)],'k-')
    ax.plot([50,100],[50*math.sqrt(3),0],'k-')
    
    # show names of the three end members
    ax.annotate('OH', xy=(0.02, 0.02), xycoords='axes fraction', fontsize=14, color = 'k',fontweight='bold',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') 

    ax.annotate('F', xy=(0.95, 0.02), xycoords='axes fraction', fontsize=14, color = 'k',fontweight='bold',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') 

    ax.annotate('Cl', xy=(0.49, 0.98), xycoords='axes fraction', fontsize=14, color = 'k', fontweight='bold',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') 

    ## plot tie lines 
    for x1 in np.arange(10,100,10):
        x2=50+0.5*x1
        y1=0
        y2=math.sqrt(3)*(x2-x1)
        x3=0.5*x1
        y3=math.sqrt(3)*x3
        ax.plot([x1,x2],[y1,y2],'silver',alpha=0.5)
        ax.plot([x1,x3],[y1,y3],'silver',alpha=0.5)
        ax.plot([x2,x2-x1],[y2,y2],'silver',alpha=0.5)

    ## plot mole fraction numbers for binaries 
    # OH-F binary
    for x1 in np.arange(20,100,20):
        y1=-4
        ax.annotate(str(x1), xy=(x1, y1), xycoords='data', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='center', va='center') 

    # OH-Cl binary
    ax.annotate(str(50), xy=(25-1, 25*np.sqrt(3)), xycoords='data', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='center', va='center') 

    # F-Cl binary
    ax.annotate(str(50), xy=(75+5, 25*np.sqrt(3)), xycoords='data', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='center', va='center') 

