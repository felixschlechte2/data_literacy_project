import pandas as pd
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import numpy as np

file = r"C:\Users\felix\Documents\M. Sc. ML\Data Literacy\analysis\fixed_effects\test_FE.csv"

df = pd.read_csv(file)

print(df)

df = df.set_index(['Year'])

# Fixed Effects Modell
mod = PanelOLS.from_formula(
    'AQ ~ A + B + C', # + EntityEffects + TimeEffects
    df
)

# Modell schätzen
res = mod.fit()

# Ergebnisse anzeigen
print(res.summary)
