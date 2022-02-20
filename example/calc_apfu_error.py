# - import modules - # 

import os, sys
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

if not os.path.exists('pyAp') and os.path.exists('../pyAp'): # hack to allow scripts to be placed in subdirectories next to pyAp:
    sys.path.insert(1, os.path.abspath('..'))

# from pyAp.ApStoic_Ketcham import stoi_ketcham, stoi_
from pyAp.ApStoic import error_

# - import module finish - #
############################################################################

# load data
data = pd.read_excel('data_ap_major_volatile.xlsx')
errors = pd.read_excel('data_ap_errors.xlsx')
# errors = pd.DataFrame(columns = ['SIO2','TIO2','AL2O3','FEO','CAO','MGO','MNO','K2O','NA2O','P2O5','SO3','CO2', 'F','CL','H2O','CE2O3','SRO'])

cal_errors = error_(data,errors,assume_oxy=26)
print('error in XOH *100%: ', 100*cal_errors['XOH_SD']/cal_errors['XOH'])

cal_errors.to_csv('output_ap_errors.csv')