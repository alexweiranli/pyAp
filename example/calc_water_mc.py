# - import modules - #
import os, sys 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
import seaborn as sns

if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))

from pyAp import pyApthermo
from pyAp.pyAp_tools import ap_mc, yes_or_no

# - import module finish - #
##############################


### Import data ####
df = pd.read_excel('data_calc_water.xlsx')

## place data columns in certain order for melt water calculation
order  = ['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL', 'MELTCOMP']
data = df[order]  

## calculate melt water contents using parameter values (ignoring errors)
results = pd.DataFrame()
list_result = data.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
results['MeltWater_calcfromF']  = [x[0] for x in list_result]
results['MeltWater_calcfromCl'] = [x[1] for x in list_result]
results['sample']               = df['sample']

fn = 'outputs_melt_water.csv'
results.to_csv(fn)

print('\n>> Results are saved in ' + fn)

## calculate errors in melt water contents consdidering errors in parameter values 
if yes_or_no("\nRun MC for error propagation?"):  

    #### +++++ Entry of MCS +++++ #####
    mc = 1000   # set mc
    print('>> Simulation starts ...')

    # if mc > 500:
    #     load_animation()

    # create dataframe for mc collection
    ap_mc_collect = pd.DataFrame([])

    comp = df[['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL']]
    std = df[['XF_SD', 'XCL_SD', 'T_SD','MELTF_SD', 'MELTCL_SD']]

    for idx in range(len(df)):

        df_iter = ap_mc(comp, std, idx, mc)
        ap_mc_collect = ap_mc_collect.append(df_iter)


    ap_mc_collect.columns = comp.columns
    ap_mc_collect['MELTCOMP'] = df.loc[df.index.repeat(mc)]['MELTCOMP']
    ap_mc_collect['water_estimates'] = ap_mc_collect.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
    ap_mc_collect['sample'] = df.loc[df.index.repeat(mc)]['sample']

    print('\n>> Simulation completed') 

    results_mc = pd.DataFrame()
    results_mc['MeltWater_calcfromF'] = [x[0] for x in ap_mc_collect['water_estimates']]
    results_mc['MeltWater_calcfromCl'] = [x[1] for x in ap_mc_collect['water_estimates']]

    results_mc['sample'] = ap_mc_collect.reset_index()['sample']

    fn_mc = 'outputs_melt_water_mc.csv'
    results_mc.to_csv(fn_mc, index=False)
    print('\n>> mc = ' + str(mc) + '. All MC results are saved in csv file: ' + fn + '\n')


    ### median calculation
    median_F = results_mc.groupby('sample')['MeltWater_calcfromF'].median()
    median_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].median()

    # ### std calculation
    sd_F = results_mc.groupby('sample')['MeltWater_calcfromF'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()
    sd_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()

    results['MeltWater_Fmedian']   = [x for x in median_F]
    results['MeltWater_F1sd']  = [x for x in sd_F]
    results['MeltWater_F_error,100%']  = results['MeltWater_F1sd']/results['MeltWater_Fmedian']*100

    results['MeltWater_Clmedian']  = [x for x in median_Cl]
    results['MeltWater_Cl1sd'] = [x for x in sd_Cl]
    results['MeltWater_Cl_error,100%']  = results['MeltWater_Cl1sd']/results['MeltWater_Clmedian']*100

    results.to_csv(fn)
    
    print(results)

    print('\n>> The median and standard deviation of MC results are saved in csv file: '+ fn)


    ### plot results ###
    fig, axes = plt.subplots(1, 2, figsize=(9,4), constrained_layout=True)

    # results_mc.dropna(inplace=True)
    sns.kdeplot(x = 'MeltWater_calcfromF', data=results_mc, hue='sample', ax = axes[0])
    sns.kdeplot(x = 'MeltWater_calcfromCl', data=results_mc, hue='sample', ax = axes[1])
  

    plt.show()


