import pandas as pd
from linearmodels.panel import PanelOLS, RandomEffects
import matplotlib.pyplot as plt
import numpy as np

file = r"C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\test_FE.csv"

df = pd.read_csv(file)

df = df.set_index(['City', 'Year'])


# Fixed Effects Modell # + EntityEffects + TimeEffects
mod = PanelOLS.from_formula(
    'AQ_diff ~ A + B + C + EntityEffects + TimeEffects', 
    data=df
)
res = mod.fit()
print(res.summary)

print("---------------------------------------------------------------------")

# rondom effects
mod_re = RandomEffects.from_formula('AQ_diff ~ A + B + C + EntityEffects + TimeEffects', data=df)
res_re = mod_re.fit()
print(res_re)
