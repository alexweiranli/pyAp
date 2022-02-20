# - import modules - # 
from codecs import ignore_errors
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))

## calculate OH mole fraction using the method of Ketcham (2015 Am.Min.)
from pyAp.ApStoic_Ketcham import stoi_ketcham, stoi_


# - import module finish - #
############################################################################

## load data and create dataframe for results
fn = 'data_ap_major_volatile.xlsx'
data = pd.read_excel(fn)

columns_user = ['SI','TI','AL','FE','CA','MG','MN','K','NA','P','S','C','XF','XCL','XOH','CE','SR','stoi,(Ca/P-5/3)/(5/3)*100%','sample']
results = pd.DataFrame(columns = columns_user)

oxy_corr_all = []
for row in range(len(data)):

    x_oh = 0
    x_oh_all = list([x_oh])

    for kk in range(50):

        x_oh = stoi_ketcham(data,row,assume_oxy = 26 - x_oh/2)

        if x_oh == x_oh_all[-1] == x_oh_all[-2]: # stop iteration when the calculated XOH does not vary  
            
            x_oh_corr = x_oh
            
            pass
        else:
            x_oh_all.append(x_oh)

    ## read the correct x_oh calculated from above    
    oxy_corr = 26 - x_oh_corr
    oxy_corr_all.append(oxy_corr)


data['OXYGEN NUMBER'] = oxy_corr_all

data.to_excel(fn, index=False)

results = stoi_(data)

print(results['XOH'])
results.to_csv('output_apfu_ketcham.csv')