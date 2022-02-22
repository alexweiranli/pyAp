"""
Weiran Li & Yishen Zhang

2022-01-20, v0.1

Please cite the paper below if you use "ApThermo" in your research:

Li and Costa (2020, GCA) https://doi.org/10.1016/j.gca.2019.10.035
"""

import scipy.optimize
import math, numpy as np, pandas as pd

MassCl  = 35.45    # Molar mass of Cl
MassF   = 18.998   # Molar mass of F
MassH2O = 18.015   # Molar mass of H2O
meanM   = 33       # Molar mass of Melt
R       = 8.314     # Universal gas constant

class ApThermo:
    """
    calculate exchange coefficients (Kd) and melt water contents using apatite

    Input values should be filled in the provided excel spreadsheet. 
    
    !! Do NOT change the column header names in the input file, as this code reads the data according to those names (it's okay to change column orders).

    Parameters ("inputs")
    --------  
    Inputs have to follow this order:  "XF", "XCL", "T,C", "MELTF", "MELTCL", "MELTCOMP",

    For Kd calculation:
    * XF  : mole fraction of F in apatite (can be calculated from "pyAp/ApStoic.py")
    * XCL : mole fraction of Cl in apatite
    * "T,C"   : temperature in celsius degree

    For water calculation (if "cal_H2O==True"):
    * MELTF   : F concentration in the melt, in wt%
    * MELTCL  : Cl concentration in the melt, in wt%
    * MELTCOMP: Melt composition (for choosing water speciation model)


    Switches (conditions for calculation)
    --------- 
    For water speciation: "highP" , "highT" (see below)
    
    "cal_H2O"  : choose whether to calculate melt water contents
                 default = True

    "cal_gamma": choose whether to calculate activity coefficients of F, Cl, OH in the melt (for further calculations beyond this model)
                 default = False 

    """

    def __init__(self,inputs,cal_H2O=True,cal_gamma=False):

        self.speciation_dict = {'dacite':         [1.49 , -2634  ],
                                'alkali basalt':  [0.641, -2704.4],
                                'rhyolite':       [1.876, -3100  ],
                                'andesite':       [1.547, -2453  ],
                                'rhyolite_highP': [1.804, -3090  ],       
                                'andesite_highT': [2.99,  -3650  ],   
                                'default':        [1.49 , -2634  ]    # dacite
                                    }
        if type(inputs) == list:
            self.x_f = float(inputs[0])
            self.x_cl = float(inputs[1])
            self.t_c  = float(inputs[2])
            self.meltf = float(inputs[3])
            self.meltcl = float(inputs[4])
            self.meltcomp = inputs[-1]
        else:
            self.x_f, self.x_cl, self.t_c, self.meltf, self.meltcl, self.meltcomp = inputs.values

        
        self.t_k        = float(self.t_c) + 273.15
        self.cal_H2O    = cal_H2O
        self.cal_gamma  = cal_gamma
     
        # calculate OH mole fraction (x_oh>0)
        self.x_oh = 1 - (self.x_cl + self.x_f)
        if self.x_oh < 0:
            self.x_oh = 0


    def Kd(self):

        """
        calculate exchange coefficients Kd using apatite F-Cl-OH composition, and temperature (T) 
        
        return Kds for OH-Cl, OH-F, Cl-F, and activity coefficients (gamma) for OH, F, Cl

        """
        # Gibbs free energy of reaction 
        deltaG_ClOH = 72.9 - 0.034 * self.t_k          # in kJ/mol
        deltaG_FOH = 94.6 - 0.04 * self.t_k           # in kJ/mol
        deltaG_ClF = deltaG_FOH - deltaG_ClOH

        # Interaction parameter Wg 
        Wg_ClOH=5;        # Wg for Cl-OH
        Wg_FOH=7;         # Wg for F-OH
        Wg_FCl=16;        # Wg for F-Cl

        # difference between two Wgs
        Wg_diff1 = Wg_FOH - Wg_FCl
        Wg_diff2 = Wg_ClOH - Wg_FCl
        Wg_diff3 = Wg_ClOH - Wg_FOH

        Kd_OHCl= math.exp((1000 * (- deltaG_ClOH - ((self.x_cl - self.x_oh) * Wg_ClOH+self.x_f * Wg_diff1)))/(R * self.t_k))
        Kd_OHF = math.exp(1000*( - deltaG_FOH - ((self.x_f - self.x_oh) * Wg_FOH + self.x_cl * Wg_diff2))/(R * self.t_k))
        Kd_ClF = Kd_OHF/Kd_OHCl

        if self.cal_gamma and self.t_c == self.t_c:  

            gammaOH=math.exp(1000 * ((self.x_cl * (1 - self.x_oh) * Wg_ClOH + self.x_f * (1 - self.x_oh) * Wg_FOH - \
                self.x_cl * self.x_f * Wg_FCl)) / (R * self.t_k))

            gammaF=math.exp(1000 * ((self.x_cl * (1 - self.x_f) * Wg_FCl + self.x_oh * (1 - self.x_f) * Wg_FOH - \
                self.x_cl * self.x_oh * Wg_ClOH)) / (R * self.t_k))

            gammaCl=math.exp(1000 * ((self.x_oh * (1 - self.x_cl) * Wg_ClOH + self.x_f * (1 - self.x_cl) * Wg_FCl - \
                self.x_f * self.x_oh * Wg_FOH)) / (R * self.t_k))

        else:
            gammaOH = gammaF = gammaCl = np.nan

        return Kd_OHCl, Kd_OHF, Kd_ClF, gammaOH, gammaF, gammaCl



    def conversion(self, moleOH_melt,k2):
        """
        convert melt OH (moles) to melt total H2O (wt%)
        
        return total H2O concentration (wt%) in the melt

        """
        ## solve the function below to calculate melt H2O (mole) using melt OH (mole)
        def func_speci(x):
            y = 2 * x + (8 * x + k2 - 2 * x * k2 - math.sqrt(k2) * math.sqrt(16 * x - 16 * x**2\
                + k2 - 4 * x * k2 + 4 * x**2 * k2)) / (k2 - 4) - moleOH_melt
            return y
        try:
            moleH2O_melt = scipy.optimize.fsolve(func_speci,0.01)
            if moleH2O_melt <0:
                moleH2O_melt = 0
        except:
            moleH2O_melt = np.nan
            

        ## solve the function below to calculate melt H2O (mole) using melt OH (mole)
        def func_wt(x):
            y = (x / MassH2O) / (x / MassH2O + (1 - x) / meanM) -  moleH2O_melt
            return y
        try:
            MeltWater = scipy.optimize.fsolve(func_wt,1)[0]   # x100 wt.%
        except:
            MeltWater = np.nan

        # set the range of melt H2O contents as between 0 and 15 wt%
        if MeltWater == MeltWater and MeltWater > 14.999/100 or MeltWater<0:   
            MeltWater = np.nan
                
        return MeltWater*100


    def meltH2O(self):
        """
        calculate water concentrations in the melt (wt%) using OH/Cl and/or OH/F in the melt and the "conversion" func written above
        
        return all results: melt water estimates, KDs, gammas 
        
        """
        if self.cal_H2O:

            # read parameters a, b for calculating equilibrium constant
            all_speciation_dict = list(self.speciation_dict)
    
            if self.meltcomp in all_speciation_dict:
                a, b = self.speciation_dict.get(self.meltcomp) # 
            else:
                a, b = self.speciation_dict['default']

            # equilibrium constnat k2 of water speciation reaction
            keq = math.exp(a + b/self.t_k)
            k2 = float(keq)
            Kd_OHCl, Kd_OHF, Kd_ClF, gammaOH, gammaF, gammaCl = self.Kd()

            # calculate molar ratios of melt OH/Cl and OH/F
            OHCl_melt = (self.x_oh / self.x_cl) / Kd_OHCl
            OHF_melt = (self.x_oh / self.x_f) / Kd_OHF

            # if melt Cl and/or melt F concentrations are provided
            moleCl_melt = ((self.meltcl/10000) / MassCl) / (100 / meanM)
            moleOH_melt_fromCl = moleCl_melt * OHCl_melt

            moleF_melt = ((self.meltf/10000) / MassF) / (100 / meanM)
            moleOH_melt_fromF = moleF_melt * OHF_melt

            # calculate melt water concentration using melt Cl and/or F
            MeltWater_Cl = self.conversion(moleOH_melt_fromCl,k2)
            MeltWater_F  = self.conversion(moleOH_melt_fromF,k2)
            
            
            return  [MeltWater_F, MeltWater_Cl,Kd_OHCl, Kd_OHF, Kd_ClF, gammaOH, gammaF, gammaCl]
