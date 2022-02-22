# Compare apfu/mole fractions calculated from 25 or 26 oxygen, and oxygen between 25 and 26 (following Ketcham 2015, Am.min.)

# - import modules - #
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import math, os, sys

# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))
from pyAp import ApTernary

##########################################################################

df_26o = pd.read_csv('outputs_apfu_26o.csv')
df_25o = pd.read_csv('outputs_apfu_25o.csv')
df_ketcham = pd.read_csv('outputs_apfu_ketcham.csv')


## plot ternary diagram
fig = plt.figure()
fig.set_size_inches(10, 8)
ApTernary.ternary(fig)


# calculate x,y coordinates of data points on the ternary diagram
colors = ['k','b','r']

# plot 
print("\n>> Calculation starts ...")
for idx, value in df_26o.iterrows():
    x_f = value['XF']
    x_cl = value['XCL']
    x = (x_f + x_cl/2) * 100
    y = x_cl*math.sqrt(3)*50
    if x > 100:
        x = 100
    if y > math.sqrt(3)*50:
        y = math.sqrt(3)*50
    plt.plot(x,y,'+',c=colors[idx],label=value['sample']+',26O')


for idx, value in df_25o.iterrows():
    x_f = value['XF']
    x_cl = value['XCL']
    x = (x_f + x_cl/2) * 100
    y = x_cl*math.sqrt(3)*50
    if x > 100:
        x = 100
    if y > math.sqrt(3)*50:
        y = math.sqrt(3)*50
    plt.plot(x,y,'x',c=colors[idx],label=value['sample']+',25O')


for idx, value in df_ketcham.iterrows():
    x_f = value['XF']
    x_cl = value['XCL']
    x = (x_f + x_cl/2) * 100
    y = x_cl*math.sqrt(3)*50
    if x > 100:
        x = 100
    if y > math.sqrt(3)*50:
        y = math.sqrt(3)*50
    plt.plot(x,y,'.',c=colors[idx],label=value['sample']+',Ketcham')


print("\n>> Close the figure to exit. ")
plt.legend(loc='best')
plt.show()
