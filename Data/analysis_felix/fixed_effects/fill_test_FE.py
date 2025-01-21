import pandas as pd
from linearmodels.panel import PanelOLS
import matplotlib.pyplot as plt
import numpy as np

# file = r"C:\Users\felix\Documents\M. Sc. ML\Data Literacy\analysis\fixed_effects\test_FE.csv"
file = r"C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\test_FE.csv"

def softmax(x):
    # Numerische Stabilität verbessern, indem wir das Maximum von x abziehen
    exp_x = np.exp(x - np.max(x))
    return exp_x / exp_x.sum(axis=0)

df = {
    'City': [],
    'AQ': [],
    'AQ_wo_parties': [],
    'Year': [],
    'A': [], 
    'B': [], 
    'C': [], 
    'AQ_diff': []
}

cities =  []

for i in range(500):
    cities.append(i)

for city in cities: 
    aq_start = 50
    for i in range(2000, 2024):
        # if i % 4 == 0:    # election every 4 years
        a = np.random.rand()
        b = np.random.rand()
        c = np.random.rand()
        elec = softmax([a,b,c])
        df['A'].append(elec[0])
        df['B'].append(elec[1])
        df['C'].append(elec[2])
        df['City'].append(city)
        df['Year'].append(i)
        aq_start -= 1 # np.random.normal(2,0.5)
        df['AQ_wo_parties'].append(aq_start)
        aq = aq_start - 2 *elec[0] + 0.5 * elec[1]
        df['AQ'].append(aq)
        if len(df['AQ']) > 1 and df['City'][-1] == df['City'][-2]:
            df['AQ_diff'].append(df['AQ'][-1] - df['AQ'][-2])
        else:
            df['AQ_diff'].append(0)
    
x = df['Year']
y = df['AQ']
y2 = df['AQ_wo_parties']

# plt.plot(x, y, label='AQ', color='blue', linestyle='-', marker='o')
# plt.plot(x, y2, label='AQ w/o influence of arties', color='red', linestyle='--', marker='s')

# # Titel und Achsenbeschriftungen hinzufügen
# plt.title('modellized aq over years')
# plt.xlabel('years')
# plt.ylabel('AQ')

# # Legende hinzufügen
# plt.legend()

# # Graph anzeigen
# plt.show()


df = pd.DataFrame(df)
df.to_csv(file, index=False, encoding="utf-8")

