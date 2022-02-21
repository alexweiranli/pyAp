# - import modules - #
import os, sys
import matplotlib.pyplot as plt
import pandas as pd
import math

# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))
    
from pyAp import ApTernary

# - import module finish - #
############################################################################

# set up a figure for ternary plot
fig = plt.figure()
fig.set_size_inches(10, 8)

# plot ternary (w/o data)  
ApTernary.ternary(fig)

## plot data in ternary diagram
# load data from csv/xlsx file 
df = pd.read_csv('outputs_apfu_26o.csv') # df = pd.read_excel('data_calc_water.xlsx')

# calculate the x,y coordinates on ternary diagram according to input XF and XCL values
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
