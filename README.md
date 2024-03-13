# pyAp

Code authors: Dr. Weiran Li (```weiranli@hku.hk```; University of Hong Kong) & Yishen Zhang (KU Leuven, Belgium) 

## Introduction  
pyAp is a python package for calculating magmatic volatile, trace element concentrations, and oxygen fugacity using mineral apatite.  More modules will be added in the future.

It includes multiple apatite-based models developed by W. Li and co-authors, including: 

* ApThermo: a thermodynamic model for calculating melt H<sub>2</sub>O (and CO<sub>2</sub>) concentrations (following Li & Costa, 2020, GCA).

  - Inputs:  Apatite F, Cl and H<sub>2</sub>O (if available) concentrations; Temperature and melt Cl and/or F concentrations (for calculating melt water).
  
  - Outputs: Apatite stoichiometry (atom per fomula unit); Exchange coefficients for OH-Cl and/or OH-F; H<sub>2</sub>O concentrations in the melt.
* ApREE: a lattice strain-thermodynamic model for calculating melt trace element (including REE) concentrations and oxygen fugacity (*fO<sub>2</sub>*) (following Li et al., 2023, CMP).

  - Inputs:  Trace element concentrations in apatite and melt (be it melt inclusions/groundmass/whole rock).
  
  - Outputs: Partition coefficients of unmeasured trace elements; oxygen fugacity of the melt (if Eu was measured).


## Documentation
Full documentation, further information about the package, and a tutorial for getting started are provided at [pyap.readthedocs.io](https://pyap.readthedocs.io/en/latest/)

## Installation
pyAp can be installed by running ```python setup.py install``` in the package depository using command line commands.

## Citing pyAp
If you use this package please cite the relevant publications for:

**ApThermo**:
Li, W. & Costa, F. (2020) A thermodynamic model for F-Cl-OH partitioning between apatite and melt including non-ideal mixing and applications to constraining melt volatile budgets, Geochimica et Cosmochimica Acta 269, 203–222. https://doi.org/10.1016/j.gca.2019.10.035. 

**ApREE**:
Li, W., Costa, F, Oppenheimer, C. & Nagashima K. (2023) Volatile and trace element partitioning between apatite and alkaline melts, Contributions to Mineralogy and Petrology 178:9. https://doi.org/10.1007/s00410-022-01985-8. 

You are encouraged to cite the specific version of the package you used. The DOI of the first zenodo release (v0.1) is
[![DOI](https://zenodo.org/badge/431824228.svg)](https://zenodo.org/badge/latestdoi/431824228)

