About pyAp
=====================================
pyAp is a python package for calculating magmatic volatile, trace element concentrations, and oxygen fugacity using mineral apatite. 

Code authors: Weiran Li (University of Cambridge, U.K.) & Yishen Zhang (KU Leuven, Belgium) 

Introduction
#########

pyAp includes multiple apatite-based models developed by W. Li and co-authors, including:

* ApThermo: a thermodynamic model for calculating melt H :sub:`2` O (and CO :sub:`2` ) concentrations (following Li & Costa, 2020, GCA)

  - Inputs:  Apatite F, Cl and H :sub:`2` O (if available) concentrations; Temperature and melt Cl and/or F concentrations (for calculating melt water)
  
  - Outputs: Apatite stoichiometry (atom per fomula unit); Exchange coefficients for OH-Cl and/or OH-F; H :sub:`2` O concentrations in the melt
  
  
* ApREE2O3: a lattice strain-thermodynamic model for calculating melt trace element (including REE) concentrations and oxygen fugacity ( *f* O :sub:`2`) (following Li et al, in review)

  - Inputs:  Trace element concentrations in apatite and melt (be it melt inclusions/groundmass/whole rock)
   
  - Outputs: Partition coefficients of unmeasured trace elements; oxygen fugacity of the melt (if Eu was measured)

* More modules will be added in the future (ApTimer - Li et al. 2020 EPSL; ApZone - Li et al. in prep). 

Citing pyAp
#########
If this package enables or aids your research please cite the relevant publications for:

**ApThermo**:
Li, W. & Costa, F. (2020) A thermodynamic model for F-Cl-OH partitioning between apatite and melt including non-ideal mixing and applications to constraining melt volatile budgets, Geochimica et Cosmochimica Acta 269, 203–222. https://doi.org/10.1016/j.gca.2019.10.035 

**ApREE2O3**:
Li, W., Costa, F, Oppenheimer, C. & Nagashima (in review) K. Measurements and a general model of volatile and trace element partitioning between apatite and alkaline melts. 

You are encouraged to cite the specific version of the package you used. The first zenodo release (v1.0) is: DOI
