import pandas as pd
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt

# file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\elec_NO2_filtered.csv'
# traffic_file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\traffic.csv'

file = r'C:\Users\felix\Documents\M. Sc. ML\Data Literacy\analysis\elec_NO2.csv'
traffic_file = r'C:\Users\felix\Documents\M. Sc. ML\Data Literacy\analysis\fixed_effects\traffic.csv'

df = pd.read_csv(file)

df_traffic = df[df['Air Quality Station Type'] == 'Traffic']
df_background = df[df['Air Quality Station Type'] == 'Background']
df_industrial = df[df['Air Quality Station Type'] == 'Industrial']

# print((len(df_traffic) + len(df_background) + len(df_industrial)) == len(df)) # this is True

df_traffic.to_csv(traffic_file, index=False, encoding="utf-8")

df_traffic = pd.read_csv(traffic_file)

df_traffic = df_traffic.set_index(['City', 'Year'])

# Fixed Effects Modell
mod = PanelOLS.from_formula(
    'Air_Pollution_Level ~ Gruene + CDU + EntityEffects + TimeEffects',
    df_traffic
)

# Modell schätzen
res = mod.fit()

# Ergebnisse anzeigen
print(res.summary)



# Koeffizienten extrahieren
coefficients = res.params[:-1]  # EntityEffects wird ausgeschlossen
coefficients.plot(kind='bar')
plt.title("Einfluss der Parteien auf die Luftqualität")
plt.ylabel("Koeffizient")
plt.show()

