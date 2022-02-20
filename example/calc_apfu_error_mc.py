import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))

# from pyAp.ApStoic_Ketcham import stoi_ketcham, stoi_
from pyAp.pyAp_tools import ap_mc
from pyAp.ApStoic import stoi_

data = pd.read_excel('data_ap_major_volatile.xlsx')
errors = pd.read_excel('data_ap_errors.xlsx')
col = data.columns[1:-3]
# results = stoi_(data,assume_oxy = 26)

mc = 1000
ap_mc_stoic = pd.DataFrame([])
ap_mc_res = pd.DataFrame([])

print('>> Simulation starts ...')

for i in range(len(data)):
    df_iter = ap_mc(data[col], errors[col], i, mc)
    ap_mc_stoic = ap_mc_stoic.append(df_iter)

ap_mc_stoic.columns = col
ap_mc_stoic['H2O'] = np.nan
ap_mc_stoic['sample'] = data.loc[data.index.repeat(mc)]['sample']
ap_mc_stoic['TOTAL'] = data.loc[data.index.repeat(mc)]['TOTAL']
ap_mc_stoic['OXYGEN NUMBER'] = data.loc[data.index.repeat(mc)]['OXYGEN NUMBER']
ap_mc_stoic = ap_mc_stoic[data.columns]
ap_mc_stoic.reset_index(inplace=True, drop=True)
ap_mc_stoic['TOTAL'] = ap_mc_stoic.iloc[:, 1:-2].sum(axis=1)



ap_mc_res = stoi_(ap_mc_stoic)
print('\n>> Simulation completed') 
ap_mc_res.groupby('sample').agg(
    ['mean', 'median', 'std']).to_excel('mc_stoic.xlsx')
