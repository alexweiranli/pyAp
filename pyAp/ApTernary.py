"""
Weiran Li & Yishen Zhang

2022-01-14, v1.0

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import matplotlib.pyplot as plt, math, numpy as np

def ternary(n):
    """
    function for ternary plot

    Parameter:
    -------
    n: :class: `numpy.array`
        numpber of figures to be plotted
    """
    
    fig, ax = plt.subplots(1)
    fig.set_size_inches(7, 5.5)

    plt.plot([0,100],[0,0],'k-');
    plt.plot([0,50],[0,50*math.sqrt(3)],'k-');
    plt.plot([50,100],[50*math.sqrt(3),0],'k-');
    plt.axis('off');

    # show names of the three end members
    plt.annotate('OH', xy=(0.02, 0.02), xycoords='axes fraction', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') ;

    plt.annotate('F', xy=(0.95, 0.02), xycoords='axes fraction', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') ;

    plt.annotate('Cl', xy=(0.49, 0.98), xycoords='axes fraction', fontsize=14, color = 'k',
                    xytext=(-5, 5), textcoords='offset points',
                    ha='left', va='top') ;

    for x1 in np.linspace(10,90,num=9):

        x2=50+0.5*x1;
        y1=0;
        y2=math.sqrt(3)*(x2-x1);
        x3=0.5*x1;
        y3=math.sqrt(3)*x3;
        plt.plot([x1,x2],[y1,y2],'silver',alpha=0.5);
        plt.plot([x1,x3],[y1,y3],'silver',alpha=0.5);
        plt.plot([x2,x2-x1],[y2,y2],'silver',alpha=0.5);

