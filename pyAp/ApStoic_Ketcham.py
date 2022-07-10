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
    data = data.copy()
    data.fillna(0, inplace=True)
    results = pd.DataFrame(columns = formulas_capt)
    bias = []
    oxygen_corr_all = []
    assume_oxy = 26
    # read data
    for row in range(len(data)):
        
        df = data.loc[data.index[row]] ## in case data.index include inconsecutive integers
        x_oh = 0
        x_oh_all = list([x_oh])

        for kk in range(50):
            assume_oxy = 26 - x_oh

        # calculate atom per formula unit
            multi_all =[]; total_oxygen=[]    
            for fm in oxides:     
                molar = pt.formula(fm).mass
                oxide = fm.upper()
                conc = df[oxide]
                
                mole_fra = conc / molar
                oxy_num =  mole_fra * dict_oxynum[oxide]
                total_oxygen.append(oxy_num)

                cat_num = dict_catnum[oxide]
                multi = mole_fra * cat_num
                multi_all.append(multi)
        
            oxygen_factor =  assume_oxy / sum(total_oxygen)
                  
            apf_f = oxygen_factor * df['F'] / pt.formula('F').mass
            apf_cl = oxygen_factor * df['CL'] / pt.formula('Cl').mass
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
           
            ## terminate iteration when the calculated XOH converges
            if kk >=2 and x_oh == x_oh_all[-1] == x_oh_all[-2]:
                break

        oxygen_corr_all.append(assume_oxy)

        apf = [mm * oxygen_factor for mm in multi_all] 
        results.loc[row] = apf
        results['F'][row] = x_f 
        results['CL'][row] = x_cl
        results['H2O'][row] = x_oh  ## note that this is actually equal to OH mole fraction, not H2O mole fraction  
        

        # test stoichiometry using molar Ca/P (=5/3)
        total_ca = sum(results.iloc[row][ca_site])
        total_phos = sum(results.iloc[row][p_site])
    
        bias.append(100 * (total_ca / total_phos - 5 / 3) / (5 / 3))    
      
        ## measured
        if data['H2O'][row]:
            mF =  data['F'][row] /pt.formula('F').mass
            mCl = data['CL'][row] /pt.formula('Cl').mass
            moh =  2 * data['H2O'][row] / pt.formula('H2O').mass
            
            total_ani_m = mF + moh + mCl
            x_f = mF/total_ani_m
            x_cl = mCl/total_ani_m
            x_oh = moh/total_ani_m
            
            # save x_f, x_cl, x_oh to the results dataframe
            results['F'][row] = x_f 
            results['CL'][row] = x_cl 
            results['H2O'][row] = x_oh

    results['stoi_bias,(Ca/P-5/3)/(5/3)*100%'] = bias
    results['sample'] = data['sample']
    results['CAL_H2O(WT%)'] = ((results["H2O"]/2)/results["F"]) * (data['F']/pt.formula("F").mass) * pt.formula("H2O").mass
    results['OXYGEN NUMBER'] = oxygen_corr_all  #data['OXYGEN NUMBER']
    results.columns = ['CA','TI','AL','FE','MG','MN','K','NA','CE','SR',
                        'P','SI','S','C','XF','XCL','XOH',
                        'stoi_bias,(Ca/P-5/3)/(5/3)*100%','sample','CAL_H2O(WT%)','OXYGEN NUMBER']

    return  results
