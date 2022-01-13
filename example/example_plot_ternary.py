import os, sys, numpy as np, matplotlib.pyplot as plt, pandas as pd, math
from pathlib import Path
# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))

from pyAp import ApTernary

ApTernary.ternary(1)

folder = Path(os.path.dirname(os.getcwd())+'/input/4ApThermo/')
df = pd.read_excel(folder / 'calc_water.xlsx')

for idx, value in df.iterrows():

    x_f = value['XF']
    x_cl = value['XCL']
    x = (x_f + x_cl/2) * 100
    y = x_cl*math.sqrt(3)*50

    if x > 100:
        x = 100
    if y > math.sqrt(3)*50:
        y = math.sqrt(3)*50
        
    plt.plot(x,y,'o',label=value['sample'])

plt.legend(loc='best')
plt.show()
