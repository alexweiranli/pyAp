# - import modules - # 
import os, sys
import pandas as pd
if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))
from pyAp.ApStoic import stoi_
############################################################################

# load data
data = pd.read_excel('data_ap_major_volatile.xlsx')
results = pd.DataFrame()

## calculate a.p.f. of cations, mole fractions of F-Cl-OH, and test stoichiometry

# using 26 oxygen [best for F-rich apatite]
results_26 = stoi_(data,assume_oxy = 26)
results_26.to_csv('outputs_apfu_26o.csv')

print('>> calculated OH of oxygen number 26:')
print(results_26['XOH'])


# using 25 oxygen [best for OH-rich apatite]
results_25 = stoi_(data,assume_oxy = 25)
results_25.to_csv('outputs_apfu_25o.csv')

print('>> calculated OH of oxygen number 25:')
print(results_25['XOH'])


print('\n >> results saved to csv!\n')
