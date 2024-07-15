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

col = ['SIO2','TIO2','AL2O3','FEO','CAO','MGO','MNO','K2O','NA2O','P2O5','SO3','CO2', 'F','CL','H2O','CE2O3','SRO']


## mc
# set up mc for error calculation
mc = 5000   # default is at least 5000
print('>> MC = ' , str(mc) , '. Sampling starts ...')

ap_mc_stoic = pd.DataFrame([]); ap_mc_res = pd.DataFrame([])
for i in range(len(data)):
    df_iter = ap_mc(data[col], errors[col], i, mc)  # sample values within uncertainty ranges for "mc" times
    ap_mc_stoic = pd.concat([ap_mc_stoic, df_iter])
  
ap_mc_stoic.columns = col

# ! make sure your sample names are all different from each other (as this affects MC sampling)
ap_mc_stoic['sample'] = data.loc[data.index.repeat(mc)]['sample']
ap_mc_stoic.reset_index(inplace=True, drop=True)

## calculate stoichiometry for all mc samples
ap_mc_res = stoi_(ap_mc_stoic)

print('\n>> Simulation completed. Results saved to "mc_stoic.csv". \n')
ap_mc_res.groupby('sample').agg(
    ['mean','median', 'std']).to_csv('mc_stoic_1507.csv')
