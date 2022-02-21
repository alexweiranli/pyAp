##### -*- import modules -*- #####
import os,sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):    # hack to allow scripts to be placed in subdirectories next to pyAp
    sys.path.insert(1, os.path.abspath('..'))
from pyAp.pyAp_tools import ap_mc
from pyAp.ApStoic import stoi_
#####################################################

# read concentration data
data = pd.read_excel('data_ap_major_volatile.xlsx')

# read errors (could be in the same file as the concentrations)
errors = pd.read_excel('data_ap_errors.xlsx')

oxides = {'SIO2','TIO2','AL2O3','FEO','CAO','MGO','MNO','K2O','NA2O','P2O5','SO3','CO2', 'F','CL','H2O','CE2O3','SRO'}
col = oxides.intersection(list(data))

## mc
# set up mc for error calculation

mc = 1000 # default = 1000; better to be >= default
print('>> MC sampling starts ...')

ap_mc_stoic = pd.DataFrame([]); ap_mc_res = pd.DataFrame([])
for i in range(len(data)):
    df_iter = ap_mc(data[col], errors[col], i, mc)  # sample values within uncertainty ranges for "mc" times
    ap_mc_stoic = ap_mc_stoic.append(df_iter)
  
ap_mc_stoic.columns = col
ap_mc_stoic['sample'] = data.loc[data.index.repeat(mc)]['sample']
ap_mc_stoic.reset_index(inplace=True, drop=True)
## calculate stoichiometry for all mc samples 
ap_mc_res = stoi_(ap_mc_stoic)

print('\n>> Simulation completed') 
ap_mc_res.groupby('sample').agg(
    ['mean', 'median', 'std']).to_csv('mc_stoic.csv')
