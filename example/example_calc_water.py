import os, sys, numpy as np, matplotlib.pyplot as plt, pandas as pd, math, random
# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))

from pathlib import Path
import seaborn as sns
import warnings
from pyAp import pyApthermo
from pyAp.pyAp_tools import load_animation

warnings.filterwarnings('ignore')

folder = Path(os.path.dirname(os.getcwd())+'/input/4ApThermo/')

df = pd.read_excel(folder / 'calc_water.xlsx')

results = pd.DataFrame(columns = {'MeltWater_F', 'MeltWater_Cl'})

## place data columns in certain order for calculation
order  = ['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL', 'MELTCOMP']
order_sd = ['XF_SD', 'XCL_SD', 'T_SD','MELTF_SD', 'MELTCL_SD']

data = df[order]  # extract data for pyApthermo calculation

results = pd.DataFrame(columns=['MeltWater(wt%,calc_from_F)','MeltWater(wt%,calc_from_Cl)', 'sample'])

###entry of MC#####
print('mc starts')
for i in range(len(df)):
    x_f = df['XF'][i]
    x_cl = df['XCL'][i]

    # melt F and Cl concentrations
    MeltF = df['MELTF'][i]
    MeltCl = df['MELTCL'][i]

    # temperature in C degree
    temp = df['T,C'][i]

    # calculate melt water contents 
    zz = pyApthermo.ApThermo(inputs=data.iloc[i],cal_H2O=True,cal_gamma=False).meltH2O()
    results = results.append({'MeltWater(wt%,calc_from_F)':zz[0],'MeltWater(wt%,calc_from_Cl)':zz[1], 'sample':df['sample'][i]},ignore_index=True)

    # errors
    x_f_err = df['XF_SD'][i]
    x_cl_err = df['XCL_SD'][i]
    T_err = df['T_SD'][i]
    MeltF_err = df['MELTF_SD'][i]
    MeltCl_err = df['MELTCL_SD'][i]
    
    n = 1000

    if n > 500:
        load_animation()

 ## --- to revise lines below
    range_v1 = np.random.normal(loc = temp, scale= T_err,size = n) 
    range_v2 = np.random.normal(loc = x_f, scale= x_f_err, size = n) 
    range_v3 = np.random.normal(loc = x_cl, scale= x_cl_err, size = n) 
    range_v4 = np.random.normal(loc = MeltCl, scale= MeltCl_err,size = n) 
    range_v5 = np.random.normal(loc = MeltF, scale= MeltF_err, size = n) 

    kk = 2000

    for mm in range(kk):

        rand = random.choices(range(n),k=3)        
        T = range_v1[rand[0]] 
        x_f = range_v2[rand[1]]
        x_cl = range_v3[rand[2]]
        # MeltCl = range_v4[rand[3]]
        # MeltF = range_v5[rand[4]]

        data['XF'] = x_f
        data['XCL'] = x_cl
        data['T,C'] = T
        data['MELTF'] = MeltF
        data['MELTCL'] = MeltCl

        zz = pyApthermo.ApThermo(inputs=data.iloc[i], cal_H2O=True,cal_gamma=False).meltH2O()

        if float(zz[0]) > 12:
            continue

        results = results.append({'MeltWater(wt%,calc_from_F)':float(zz[0]),'MeltWater(wt%,calc_from_Cl)':float(zz[1]), 'sample':df['sample'][i]},ignore_index=True)
        

results.to_csv('output_results/calc_water_loop.csv')
print(' >> results saved to csv!\n')

fig, axes = plt.subplots(1, 2, figsize=(9,4), constrained_layout=True)

# plot
sns.kdeplot(x = 'MeltWater(wt%,calc_from_F)', data=results, hue='sample', ax = axes[0])
sns.kdeplot(x = 'MeltWater(wt%,calc_from_Cl)', data=results, hue='sample', ax = axes[1])

plt.show()
