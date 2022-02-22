print('\n>> loading ... \n')
# - import modules - # 
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math 
import seaborn as sns
if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))
# pyAp related modules (available after installing pyAp by typing in the terminal window: python3 setup.py install)
from pyAp import ApTernary
from pyAp import pyApthermo
import pyAp.pyAp_tools as tools
from pyAp.ApStoic import stoi_

# - import module finish - #
############################################################################

instruction = 'Close the plot window for next step. Before closing it you could save the plot by clicking on the "save" button in the same window.'

# set the number of mc if it will be run; default = 1000
mc = 1000   

# load data
dff = pd.read_excel('data_calc_water.xlsx')
data = pd.read_excel('data_ap_major_volatile.xlsx')

# default parameter for calculation
MeltF_def       = 800
MeltCl_def      = 2000
temp_def        = 950
meltcomp_def    = 'dacite'

results0 = pd.DataFrame()

if tools.yes_or_no("\nCalculate mole fractions and a.p.f.u. ?"):    
# calculate a.p.f., F-Cl mole fractions, and stoichiometry
    results = stoi_(data)
    results0 = results
    results.to_csv('output_apfu_allin1.csv')
    print('\n >> results saved to csv!\n')

    # print results in terminal/jupyter
    if len(results)<50:
        print(results)

else:
    results = dff

## plot apatite in ternary diagram if the user choose to (type in "y" in terminal)
if tools.yes_or_no("\nPlot F-Cl-OH ternary ?"):
    print(instruction)

#     set up figure for ternary plot
    fig = plt.figure()
    fig.set_size_inches(10, 8)
    ApTernary.ternary(fig) 
    
    for idx, value in results.iterrows():
        x_f = value['XF']
        x_cl = value['XCL']
        x = (x_f + x_cl/2) * 100
        y = x_cl*math.sqrt(3)*50

        if x > 100:
            x = 100
        if y > math.sqrt(3)*50:
            y = math.sqrt(3)*50
            
        plt.plot(x,y,'o',label=value['sample'])

    plt.legend(loc='best')
    plt.show()
        
## calculate melt H2O contents if the user choose to (type in "y" in terminal)
if tools.yes_or_no("\nCalculate melt H2O concentraion?"):

    results = pd.DataFrame(columns=['MeltWater_calcfromF','MeltWater_calcfromCl', 'sample'])
    
    if results0.empty != True:      
        if tools.yes_or_no("\nUse mole fractions just calculated? If not, those in 'data_calc_water.xlsx' will be used."):
            dff['XF']  = results0['XF']
            dff['XCL'] = results0['XCL']
    
        ## place data columns in certain order for melt water calculation
        order  = ['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL', 'MELTCOMP']
        data_for_thermo = dff[order]  

        ## calculate melt water contents using parameter values (ignoring errors)
        results = pd.DataFrame()
        list_result = data_for_thermo.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
        results['MeltWater_calcfromF']  = [x[0] for x in list_result]
        results['MeltWater_calcfromCl'] = [x[1] for x in list_result]
        results['sample']               = dff['sample']

        fn = 'outputs_melt_water_allin1.csv'
        results.to_csv(fn)

        ## calculate errors in melt water contents consdidering errors in parameter values 
        if tools.yes_or_no("\nRun MC for error propagation?"):  

            #### +++++ Entry of MCS +++++ #####            
            print('>> Simulation starts ...')

            # create dataframe for mc collection
            ap_mc_collect = pd.DataFrame()
            results_mc = pd.DataFrame(); results = pd.DataFrame()

            comp = dff[['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL']]
            std = dff[['XF_SD', 'XCL_SD', 'T_SD','MELTF_SD', 'MELTCL_SD']]

            for idx in range(len(dff)):
                df_iter = tools.ap_mc(comp, std, idx, mc)
                ap_mc_collect = ap_mc_collect.append(df_iter)

            ap_mc_collect.columns = comp.columns
            ap_mc_collect['MELTCOMP'] = dff.loc[dff.index.repeat(mc)]['MELTCOMP']
            ap_mc_collect['water_estimates'] = ap_mc_collect.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
            ap_mc_collect['sample'] = dff.loc[dff.index.repeat(mc)]['sample']

            print('\n>> Simulation completed') 

            results_mc['MeltWater_calcfromF'] = [x[0] for x in ap_mc_collect['water_estimates']]   ## only take melt water estimates between 0 and 16wt%
            results_mc['MeltWater_calcfromCl'] = [x[1] for x in ap_mc_collect['water_estimates']]  ## only take melt water estimates between 0 and 16wt%
            results_mc['sample'] = ap_mc_collect.reset_index()['sample']

#             fn_mc = 'outputs_melt_water_mc_allin1.csv'
#             results_mc.to_csv(fn_mc, index=False)
#             print('\n>> mc = ' + str(mc) + '. All MC results are saved in csv file: ' + fn + '\n')

            ### median calculation
            results_mc.fillna(0)
            results_mc = results_mc[results_mc['MeltWater_calcfromF']>0]
            median_F = results_mc.groupby('sample')['MeltWater_calcfromF'].median()
            sd_F = results_mc.groupby('sample')['MeltWater_calcfromF'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()

            results_mc = results_mc[results_mc['MeltWater_calcfromCl']>0]
            median_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].median()
            sd_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()

            results['MeltWater_Fmedian']   = [x for x in median_F if x==x]
            results['MeltWater_F1sd']  = [x for x in sd_F if x==x]

            # results['MeltWater_F_error,100%']  = results['MeltWater_F1sd']/results['MeltWater_Fmedian']*100

            results['MeltWater_Clmedian']  = [x for x in median_Cl if x==x]
            results['MeltWater_Cl1sd'] = [x for x in sd_Cl if x==x]

            results.to_csv(fn)
            
            print(results)
            print('\n>> The median and standard deviation of MC results are saved in csv file: '+ fn)
            print(instruction)
            
            
            ### plot results ###
            fig, axes = plt.subplots(1, 2, figsize=(9,4), constrained_layout=True)      
            # results_mc.dropna(inplace=True)
            sns.kdeplot(x = 'MeltWater_calcfromF', data=results_mc, hue='sample', ax = axes[0])
            sns.kdeplot(x = 'MeltWater_calcfromCl', data=results_mc, hue='sample', ax = axes[1])
    
            plt.show()
    
    if len(results)<50:
        print(results)
