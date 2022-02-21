"""
Weiran Li & Yishen Zhang

2022-01-14, v1.0

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import pandas as pd
import math 

## molar mass of each oxide
dict_molar = {'SIO2':60.08,'TIO2':79.87,'AL2O3':101.96,'FEO':71.84,'CAO':56.08,'MGO':40.30,'MNO':70.94,'K2O':94.20,'NA2O':61.98,'P2O5': 141.94,
              'SO3':80.06,'CO2':44.01, 'F':18.998,'CL':35.453,'H2O':18.015,'CE2O3':328.24,'SRO':103.62}

## number of oxygen in each oxide
dict_oxynum = {'SIO2':2,'TIO2':2,'AL2O3':3,'FEO':1,'CAO':1,'MGO':1,'MNO':1,'K2O':1,'NA2O':1,'P2O5': 5,
                'SO3':3, 'CO2':2, 'F':0.5, 'CL': 0.5, 'H2O': 2,
                'CE2O3':3, 'SRO':1}

## number of cation in each oxide
dict_catnum = {'SIO2':1,'TIO2':1,'AL2O3':2,'FEO':1,'CAO':1,'MGO':1,'MNO':1,'K2O':2,'NA2O':2,'P2O5': 2,
                'SO3':1, 'CO2':1, 'F':0, 'CL': 0, 'H2O': 0,
                'CE2O3':2, 'SRO':1}
## read oxide names
oxides = list(dict_molar)
      
def stoi_(data,assume_oxy=26):  
    """
    function to test apatite stoichiometry 

    Parameters:
    -------
    data: :class: `pandas.Dataframe`
    oxygen number: default is 26 for FAp 
                   For OHAp: use 25

    Return:
    -------
    results: :class: `pandas.Dataframe`
            saved csv file
    """
    
    data = data.copy()
    data.fillna(0, inplace=True)  # replace NaN cell to 0
    # calculate atom per formula unit
    results = pd.DataFrame(columns = oxides)
    bias = []
    
    for i in range(len(data)):
        
        multi_all = []
        total_oxygen = []
        
        for oxide in oxides:     
            molar = dict_molar[oxide]
            conc = data[oxide][i]
            
            mole_fra = conc / molar
            oxy_num =  mole_fra * dict_oxynum[oxide]
            total_oxygen.append(oxy_num)

            cat_num = dict_catnum[oxide]
            multi = mole_fra * cat_num
            multi_all.append(multi)
        
        oxygen_factor =  assume_oxy/sum(total_oxygen)
        apf = [mm * oxygen_factor for mm in multi_all] 
    
        results.loc[i] = apf
        # test stoichiometry using molar Ca/P (=5/3)
        total_ca = sum(results.iloc[i][oxides[:9]])
        total_phos = sum(results.iloc[i][oxides[9:12]])
    
        bias.append(100 * abs(total_ca / total_phos - 5 / 3) / (5 / 3))
        # if F and Cl were measured
        if data['F'][i] and data['CL'][i]:
          # if H2O was not measured
          if data['H2O'][i] == 0:  # set to == 0 as NaN has been changed to 0 above.
              apf_f = oxygen_factor * data['F'][i] / dict_molar['F']
              apf_cl = oxygen_factor * data['CL'][i] / dict_molar['CL']
              x_f = apf_f / 2
              x_cl = apf_cl / 2
              x_oh = 1 - x_f - x_cl
          # if H2O was measured
          else:
              mF =  data['F'][i] / dict_molar['F']
              mCl = data['CL'][i] / dict_molar['CL']
              moh =  2 * data['H2O'][i] / dict_molar['H2O']    
              total_ani_m = mF + moh + mCl
              x_f = mF / total_ani_m
              x_cl = mCl / total_ani_m
              x_oh = moh / total_ani_m
        else:
              x_f = x_cl = x_oh = 0
        
        # save x_f, x_cl, x_oh to the results dataframe
        results['F'][i] = x_f 
        results['CL'][i] = x_cl 
        results['H2O'][i] = x_oh


    results['stoic,(Ca/P-5/3)/(5/3)*100%'] = bias
    results['sample'] = data['sample']
    results.columns = ['SI','TI','AL','FE','CA','MG','MN','K','NA',
                        'P','S','C','XF','XCL','XOH','CE','SR','stoi,(Ca/P-5/3)/(5/3)*100%','sample']
      
    return  results
