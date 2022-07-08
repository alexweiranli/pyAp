# - import modules - # 
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))
## calculate OH mole fraction using the method of Ketcham 2015, Am.Min.
from pyAp.ApStoic_Ketcham import stoi_ketcham

############################################################################

## load data and create dataframe for results
fn = 'data_ap_major_volatile.xlsx'
data = pd.read_excel(fn)

# calculate stoichiometry following Ketcham (2015)
results = stoi_ketcham(data)

# print results 
print(results)
print(results['XOH'])

# save results to csv file
fn='outputs_apfu_ketcham.csv'
results.to_csv(fn)

print('\n >> results saved to', fn, '\n')
