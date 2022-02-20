# - import modules - # 
from codecs import ignore_errors
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))

## calculate OH mole fraction using the method of Ketcham (2015 Am.Min.)
from pyAp.ApStoic_Ketcham import stoi_ketcham


# - import module finish - #
############################################################################

## load data and create dataframe for results
fn = 'data_ap_major_volatile.xlsx'
data = pd.read_excel(fn)

results = stoi_ketcham(data)

print(results['XOH'])
results.to_csv('outputs_apfu_ketcham.csv')
