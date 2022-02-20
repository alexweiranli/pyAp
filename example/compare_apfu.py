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

# plt.plot(df['XOH'],df_ketcham['XOH'],'o')
# plt.plot([0,0.5],[0,0.5],'k--')

# plt.xlabel('26 Oxygen')
# plt.ylabel('26-[OH]/2, following Ketcham 2015')
# plt.show()

ApTernary.ternary(1)

# calculate the x,y coordinates on ternary diagram according to input XF and XCL values
colors = ['k','b','r']

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

plt.legend(loc='best')
plt.show()
