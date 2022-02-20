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


## plot 1 ternary template (no data) 
ApTernary.ternary(1)

## plot data in ternary diagram
# read data, choose from files below 

# df = pd.read_excel('data_calc_water.xlsx')
df = pd.read_csv('output_apfu.csv')

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
