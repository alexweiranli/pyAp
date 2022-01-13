import os, sys, pandas as pd, math, random, numpy as np, matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns, warnings
#############################################################################
# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))

from pyAp import pyApthermo
from pyAp.pyAp_tools import ap_mc, load_animation

warnings.filterwarnings('ignore')
    

### Import data ####
folder = Path(os.path.dirname(os.getcwd())+'/input/4ApThermo/')
df = pd.read_excel(folder / 'calc_water.xlsx')
results = pd.DataFrame(columns = {'MeltWater_F', 'MeltWater_Cl'})

## place data columns in certain order for calculation
order  = ['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL', 'MELTCOMP']
  
data = df[order]  # extract data for pyApthermo calculation

list_result = data.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
results['MeltWater_F'] = [x[0] for x in list_result]
results['MeltWater_Cl'] = [x[1] for x in list_result]
results['sample'] = df['sample']

results.to_csv('output_results/mc_median_calc_water.csv')

## 

#### +++++ Entry of MCS +++++ #####
mc = 1000 # set mc
print('mc starts')

if mc > 500:
    load_animation()

# create dataframe for mc collection
ap_mc_collect = pd.DataFrame([])

comp = df[['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL']]
std = df[['XF_SD', 'XCL_SD', 'T_SD','MELTF_SD', 'MELTCL_SD']]

for idx in range(len(df)):

    df_iter = ap_mc(comp, std, idx, mc)
    ap_mc_collect = ap_mc_collect.append(df_iter)


ap_mc_collect.columns = comp.columns
ap_mc_collect['MELTCOMP'] = df.loc[df.index.repeat(mc)]['MELTCOMP']
ap_mc_collect['zz'] = ap_mc_collect.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
ap_mc_collect['sample'] = df.loc[df.index.repeat(mc)]['sample']


results_mc = pd.DataFrame(columns=['MeltWater_F','MeltWater_Cl'])
results_mc['MeltWater_F'] = [x[0] for x in ap_mc_collect['zz']]
results_mc['MeltWater_Cl'] = [x[1] for x in ap_mc_collect['zz']]

results_mc['sample'] = ap_mc_collect.reset_index()['sample']

results_mc.to_csv('output_results/mc_calc_water.csv', index=False)
print('\n >> ' + str(mc) + ' mc completed! results saved to csv!\n')

### plot results ###
fig, axes = plt.subplots(1, 2, figsize=(9,4), constrained_layout=True)
# results_mc.dropna(inplace=True)
sns.kdeplot(x = 'MeltWater_F', data=results_mc, hue='sample', ax = axes[0])
sns.kdeplot(x = 'MeltWater_Cl', data=results_mc, hue='sample', ax = axes[1])


MeltWater_F_median = results_mc.groupby('sample')['MeltWater_F'].median()
MeltWater_Cl_median = results_mc.groupby('sample')['MeltWater_Cl'].median()

### median calculation
print(results_mc.groupby('sample')['MeltWater_F'].median())
print(results_mc.groupby('sample')['MeltWater_Cl'].median())
plt.savefig('output_results/plot_results.pdf', dpi=300)

plt.show()

### std calculation
results_mc.groupby('sample')['MeltWater_Cl'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()
results_mc.groupby('sample')['MeltWater_F'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()
