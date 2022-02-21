# Calculate apatite saturation temperature using empirical eq of Harrison and Watson 1984
import math
import numpy as np

def AST(cSiO2,cP2O5):
    """"
    Input: 
    melt SiO2, P2O5 concentrations in weight percent * 100% 
    i.e., values between 0 and 100

    Output: 
    T in Celsius degree
    """
    if cSiO2 <1:
        print('>> Warning: Concentrations are expressed as mass fractions. \nMultiply them by 100 to convert into percentage!')
        T_C = np.nan
    else:   
        T_C=(26400*cSiO2/100 - 4800)/(12.4*cSiO2/100 - math.log(cP2O5/100) - 3.97) - 273.15

    return T_C