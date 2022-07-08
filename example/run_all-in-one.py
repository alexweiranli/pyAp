print('\n>> loading ... \n')
# - import modules - # 
import os, sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math 
import seaborn as sns

# import pyAp package and modules ## you could also install the package by typing: "python3 setup.py install" in terminal window
if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))
from pyAp import ApTernary
from pyAp import pyApthermo
import pyAp.pyAp_tools as tools
from pyAp.ApStoic import stoi_

# - import module finish - #
############################################################################

instruction = '\n >> !! Close the plot window for next step. Before closing it you could save the plot by clicking on the "save" button in the same window. \n'

# load data
dff = pd.read_excel('data_calc_water.xlsx')
data = pd.read_excel('data_ap_major_volatile.xlsx')

# default parameter for calculation
MeltF_def       = 800
MeltCl_def      = 2000
temp_def        = 950
meltcomp_def    = 'dacite'

results0 = pd.DataFrame()

if tools.yes_or_no("\n Calculate mole fractions and a.p.f.u. ? "):    
# calculate a.p.f., F-Cl mole fractions, and stoichiometry
    results = stoi_(data)
    results0 = results
    pd.concat([data,results0],axis=1).to_csv('output_apfu_allin1.csv')
    print('\n >> results saved to csv!\n')

    # print results in terminal/jupyter
    if len(results)<50:
        print(results)

else:
    results = dff

## plot apatite in ternary diagram if the user choose to (type in "y" in terminal)
if tools.yes_or_no("\n\nPlot F-Cl-OH ternary ? "):

    print(instruction)

#     set up figure for ternary plot
    fig, ax = plt.subplots(figsize=(10, 8))
    ApTernary.ternary(ax)

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
if tools.yes_or_no("\nCalculate melt H2O concentraion? "):

    results = pd.DataFrame(index=range(len(data)),
                        columns=['sample','Model_used','MeltWater_calcfromF','MeltWater_calcfromCl', 
                                'MC_MeltWater_Fmedian','MC_MeltWater_F1sd','MC_MeltWater_Clmedian','MC_MeltWater_Cl1sd'])
    
    if results0.empty != True:      
        if tools.yes_or_no("\nUse mole fractions just calculated ? If not, those in 'data_calc_water.xlsx' will be used. "):
            dff['XF']  = results0['XF']
            dff['XCL'] = results0['XCL']
    
        ## place data columns in certain order for melt water calculation
        order  = ['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL', 'MELTCOMP']
        data_for_thermo = dff[order]  

        ## calculate melt water contents using parameter values (ignoring errors)
        list_result = data_for_thermo.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
        results['MeltWater_calcfromF']  = [x[0] for x in list_result]
        results['MeltWater_calcfromCl'] = [x[1] for x in list_result]
        results['Model_used']           = [x[-1] for x in list_result] # save the speciation models used
        results['sample']               = dff['sample']
    
        ## calculate errors in melt water contents consdidering errors in parameter values 
        if tools.yes_or_no('\nCalculate errors using MC sampling ? '):
            
            newmc=input('Enter total number of MC sampling (better to be >=5000) : ')
            mc = int(newmc)
            if mc>5e4:
                mc=5000
                print('MC is too large (= long simulation time). A default value (=5000) is used. \n')

            #### +++++ Entry of MCS +++++ #####            
            print('\n>> Running MC ... \n')

            # create dataframe for mc collection
            ap_mc_collect = pd.DataFrame()
            results_mc = pd.DataFrame(); 

            comp = dff[['XF', 'XCL', 'T,C', 'MELTF', 'MELTCL']]
            std = dff[['XF_SD', 'XCL_SD', 'T_SD','MELTF_SD', 'MELTCL_SD']]

            for idx in range(len(dff)):
                df_iter = tools.ap_mc(comp, std, idx, mc)
                ap_mc_collect = ap_mc_collect.append(df_iter)

            ap_mc_collect.columns = comp.columns
            ap_mc_collect['MELTCOMP'] = dff.loc[dff.index.repeat(mc)]['MELTCOMP']
            ap_mc_collect['water_estimates'] = ap_mc_collect.apply(lambda row: pyApthermo.ApThermo(inputs=row[order], cal_H2O=True,cal_gamma=False).meltH2O(),axis=1)
            ap_mc_collect['sample'] = dff.loc[dff.index.repeat(mc)]['sample']

            results_mc['MeltWater_calcfromF'] = [x[0] for x in ap_mc_collect['water_estimates']]   ## only take melt water estimates between 0 and 16wt%
            results_mc['MeltWater_calcfromCl'] = [x[1] for x in ap_mc_collect['water_estimates']]  ## only take melt water estimates between 0 and 16wt%
            results_mc['sample'] = ap_mc_collect.reset_index()['sample']                 # save sample names

            ### median calculation
            results_mc=results_mc.fillna(0)
            median_F = results_mc.groupby('sample')['MeltWater_calcfromF'].median()
            sd_F = results_mc.groupby('sample')['MeltWater_calcfromF'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()

            median_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].median()
            sd_Cl = results_mc.groupby('sample')['MeltWater_calcfromCl'].transform(lambda s: (np.percentile(s, 84)-np.percentile(s, 16))/2).unique()

            # print(results_mc, median_F, median_Cl)

            results['MC_MeltWater_Fmedian']    =  median_F.values
            results['MC_MeltWater_F1sd']       =  sd_F
            results['MC_MeltWater_Clmedian']   =  median_Cl.values
            results['MC_MeltWater_Cl1sd']      =  sd_Cl

            print(instruction)
            
            ### plot MC-sampling results ###
            fig, axes = plt.subplots(1, 2, figsize=(9,4), constrained_layout=True)      
            sns.kdeplot(x = 'MeltWater_calcfromF', data=results_mc, hue='sample', ax = axes[0])
            sns.kdeplot(x = 'MeltWater_calcfromCl', data=results_mc, hue='sample', ax = axes[1])
    
            plt.show()

    if len(results)<50:
        print('\n>>Calculated melt water contents: \n',results , '\n')

    fn = 'outputs_melt_water_allin1.csv'

    results=results.reset_index(drop=True)
    pd.concat([dff,results],axis=1).to_csv(fn)   

    print('\n>> All calculated water contents are saved in: '+ fn + '\n\n' )
