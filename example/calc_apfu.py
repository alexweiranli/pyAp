# - import modules - # 

import os, sys
import pandas as pd

if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))

from pyAp.ApStoic import stoi_

# - import module finish - #
############################################################################

# load data
data = pd.read_excel('data_ap_major_volatile.xlsx')
results = pd.DataFrame()

# calculate a.p.f., F-Cl mole fractions, and stoichiometry
results = stoi_(data,assume_oxy = 26) 
results.to_csv('output_apfu_26o.csv')
print('\n >> results saved to csv!\n')

print(results['XOH'])
# print results in terminal/jupyter
# if len(results)<50:
#     print(results)
