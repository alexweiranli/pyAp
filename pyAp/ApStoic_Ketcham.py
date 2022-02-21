"""
Weiran Li & Yishen Zhang

2022-02-20, v1.0

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import pandas as pd

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

    
# when concentration value is not provided, replace it with 0; otherwise, keep its value.
def conc_(v):
    if v == v:
        return v
    elif type(v) != float or int:
          return 0
    else:
        return 0
      
def stoi_ketcham(data):  
    """
    function to calculate apatite apfu and test stoichiometry 
    calculations following Ketcham 2015, Am. min. 

    Parameters:
    -------
    data: :class: `pandas.Dataframe`

    Return:
    -------
    results: :class: `pandas.Dataframe`

    """
    
    results = pd.DataFrame(columns = oxides)
    bias = []; oxygen_corr_all = []
    assume_oxy = 26

    # read data
    for row in range(len(data)):
        
        df = data.loc[row]
        x_oh = 0
        x_oh_all = list([x_oh])

        for kk in range(50):
            assume_oxy = 26 - x_oh

        # calculate atom per formula unit
            multi_all =[]; total_oxygen=[]    
            for oxide in oxides:     
                molar = dict_molar[oxide]
                conc = conc_(df[oxide])
                
                mole_fra = conc/molar
                oxy_num =  mole_fra * dict_oxynum[oxide]
                total_oxygen.append(oxy_num)

                cat_num = dict_catnum[oxide]
                multi = mole_fra*cat_num
                multi_all.append(multi)
        
            oxygen_factor =  assume_oxy/sum(total_oxygen)
                  
            apf_f = oxygen_factor * conc_(df['F'])/dict_molar['F']
            apf_cl = oxygen_factor * conc_(df['CL'])/dict_molar['CL']
            x_f = apf_f/2
            x_cl = apf_cl/2
            x_oh = 1 - x_f - x_cl

            if kk >=2 and x_oh == x_oh_all[-1] == x_oh_all[-2]:
                # x_oh_corr = x_oh
                break

        oxygen_corr_all.append(assume_oxy)

        apf = [mm*oxygen_factor for mm in multi_all] 
        results.loc[row] = apf
        results['F'][row] = x_f 
        results['CL'][row] = x_cl
        results['H2O'][row] = x_oh

        # test stoichiometry using molar Ca/P (=5/3)
        total_ca = sum(results.iloc[row][oxides[:9]])
        total_phos = sum(results.iloc[row][oxides[9:12]])
        bias.append(100*abs(total_ca/total_phos - 5/3)/(5/3))        

        if data['H2O'][row] == data['H2O'][row]:
            mF =  data['F'][i]/dict_molar['F']
            mCl = data['CL'][i]/dict_molar['CL']
            moh =  2 * data['H2O'][i]/dict_molar['H2O']
            
            total_ani_m = mF + moh + mCl
            x_f = mF/total_ani_m
            x_cl = mCl/total_ani_m
            x_oh = moh/total_ani_m
            
            ## save x_ to results dataframe
            results['F'][row] = x_f 
            results['CL'][row] = x_cl 
            results['H2O'][row] = x_oh

    results['OXYGEN NUMBER'] = oxygen_corr_all #data['OXYGEN NUMBER']
    results['stoic,(Ca/P-5/3)/(5/3)*100%'] = bias
    results['sample'] = data['sample']

    results.columns = ['SI','TI','AL','FE','CA','MG','MN','K','NA',
                        'P','S','C','XF','XCL','XOH','CE','SR','OXYGEN NUMBER','stoi,(Ca/P-5/3)/(5/3)*100%','sample']


    return  results
