"""
Weiran Li & Yishen Zhang

2022-07-08, v0.2

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import pandas as pd
import periodictable as pt 

## molar mass of each oxide
formulas=["CaO","TiO2","Al2O3","FeO","MgO","MnO","K2O","Na2O","Ce2O3","SrO","P2O5","SiO2","SO3","CO2","F","Cl","H2O"]
formulas_capt = [fm.upper() for fm in formulas]

# cations at calcium site
ca_site= formulas_capt[:10]
# cations at phosphorus site
p_site = formulas_capt[10:13]

## number of oxygen in each oxide
dict_oxynum = {'CAO':1,'TIO2':2,'AL2O3':3,'FEO':1,'MGO':1,'MNO':1,'K2O':1,'NA2O':1,'CE2O3':3, 'SRO':1,
                'P2O5': 5,'SIO2':2, 'SO3':3,
                'CO2':2, 'F':0.5, 'CL': 0.5, 'H2O': 2,
                }

## number of cation in each oxide
dict_catnum = {'CAO':1,'TIO2':1,'AL2O3':2,'FEO':1,'MGO':1,'MNO':1,'K2O':2,'NA2O':2,'CE2O3':2, 'SRO':1,
                'P2O5': 2,'SIO2':1, 'SO3':1,
                'CO2':1, 'F':0, 'CL': 0, 'H2O': 0,
                }

## read oxide names
oxides = formulas
      
def stoi_(data,assume_oxy=26):  
    """
    function to test apatite stoichiometry 

    Parameters:
    -------
    data: :class: `pandas.Dataframe`
    oxygen number: default is 26 for FAp, and 25 for OHAp
    [Use "ApStoic_Ketcham.py" if you wish to use oxygen number depending on the crystal composition (between 25-26) following Ketcham2015]

    Return:
    -------
    results: :class: `pandas.Dataframe`
            saved csv file
    """
    
    data = data.copy()
    data.fillna(0, inplace=True)  # replace NaN cell to 0
    results = pd.DataFrame(columns=formulas_capt.append("CAL_H2O(WT%)"))
    bias = []
    
    # calculate atom per formula unit for each row in input dataframe
    for i in range(len(data)):
        
        multi_all = []
        total_oxygen = []
        
        for fm in oxides:     
            molar = pt.formula(fm).mass
            oxide = fm.upper()
            conc = data[oxide][data.index[i]]
            
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
        total_ca = sum(results.iloc[i][ca_site])
        total_phos = sum(results.iloc[i][p_site])
    
        bias.append(100 * (total_ca / total_phos - 5 / 3) / (5 / 3))

        # if F and Cl were measured
        if data['F'][data.index[i]] and data['CL'][data.index[i]]:
          # if H2O was not measured # (** set to == 0 as NaN has been changed to 0 above)
          if data['H2O'][data.index[i]] == 0:  
              apf_f = oxygen_factor * data['F'][data.index[i]] / pt.formula('F').mass
              apf_cl = oxygen_factor * data['CL'][data.index[i]] / pt.formula('Cl').mass
              x_f = apf_f / 2
              x_cl = apf_cl / 2
              
              ## set the range of mole fractions (i.e. 0<=x<=1)
              if x_f>1:
                  x_cl=x_oh=0
                  assume_oxy=26
                  break

              elif x_cl>1:
                  x_f=x_oh=0
                  assume_oxy=26
                  break

              elif x_f + x_cl > 1:
                  x_oh=0
                  x_f=x_f/(x_f+x_cl)
                  x_cl=x_cl/(x_f+x_cl)
                  assume_oxy=26
                  break

              else:
                  x_oh = 1 - x_f - x_cl
              
          # if H2O was measured
          else:
              mF =  data['F'][data.index[i]] / pt.formula('F').mass
              mCl = data['CL'][data.index[i]] / pt.formula('Cl').mass
              moh =  2 * data['H2O'][data.index[i]] / pt.formula('H2O').mass 
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
        
        if x_oh>0:
          if x_f>0:
            results.loc['CAL_H2O(WT%)',i] = (x_oh/x_f) * (data['F'][data.index[i]]/pt.formula("F").mass) * pt.formula("H2O").mass
          else:
            if x_cl>0:
              results.loc['CAL_H2O(WT%)',i] = (x_oh/x_cl) * (data['CL'][data.index[i]]/pt.formula("Cl").mass) * pt.formula("H2O").mass
              
    results['stoi_bias,(Ca/P-5/3)/(5/3)*100%'] = bias
    results['sample'] = list(data['sample'])
    results.columns = ['CA','TI','AL','FE','MG','MN','K','NA','CE','SR',
                        'P','SI','S','C','XF','XCL','XOH','CAL_H2O(WT%)',
                        'stoi_bias,(Ca/P-5/3)/(5/3)*100%','sample']
    
    return  results
