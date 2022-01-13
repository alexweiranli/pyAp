import os, sys, numpy as np, matplotlib.pyplot as plt, pandas as pd
from pathlib import Path
# hack to allow scripts to be placed in subdirectories next to pyAp:
if not os.path.exists('pyAp') and os.path.exists('../pyAp'):
    sys.path.insert(1, os.path.abspath('..'))

from pyAp.ApStoic import stoi_

folder = Path(os.path.dirname(os.getcwd())+'/input/4ApThermo/')
data = pd.read_excel(folder / 'data.xlsx')
results = stoi_(data)

print(' >> results saved to csv!\n')
