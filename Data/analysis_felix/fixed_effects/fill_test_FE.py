import pandas as pd
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import numpy as np

file = r"C:\Users\felix\Documents\M. Sc. ML\Data Literacy\analysis\fixed_effects\test_FE.csv"

df = {
    'AQ': [],
    'Year': [],
    'A': [], 
    'B': [], 
    'C': []
}

for i in range(2000, 2024):
    df['Year'].append(i)
    a = np.random.rand()
    b = np.random.rand()
    c = np.random.rand()
    df['A'].append(a)
    df['B'].append(b)
    df['C'].append(c)
    df['AQ'].append(2 * a - b)

df = pd.DataFrame(df)
df.to_csv(file, index=False, encoding="utf-8")

df_traffic = pd.read_csv(file)

df_traffic = df_traffic.set_index(['Year'])

# Fixed Effects Modell
mod = PanelOLS.from_formula(
    'AQ ~ A + B + C', # + EntityEffects + TimeEffects
    df_traffic
)

# Modell schätzen
res = mod.fit()

# Ergebnisse anzeigen
print(res.summary)
