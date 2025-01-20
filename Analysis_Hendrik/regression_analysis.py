import pandas as pd
from scipy import stats
import numpy as np
from matplotlib import pyplot as plt

offset = 5
party = 'SPD'

election_data = pd.read_csv('../Data/election_data.csv')
PM10_data = pd.read_csv('../Data/AirPollution/processed/PM10.csv')
PM10_data = PM10_data[['Air Quality Station EoI Code', 'Year', 'Air Pollution Level', 'City']]
PM10_data = PM10_data.groupby(['Air Quality Station EoI Code', 'Year', 'City'], as_index=False).mean()

data = pd.merge(election_data, PM10_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

data = data[['Air Quality Station EoI Code', party, 'Date', 'Air Pollution Level', 'City']]

data = data[data[party] != 0]
data['Date'] = pd.to_numeric(data['Date'])

x = []
y = []

for index, row in data.iterrows():
    station = row['Air Quality Station EoI Code']
    year = row['Date']
    if PM10_data[(PM10_data['Air Quality Station EoI Code'] == station) & (PM10_data['Year'] == year + offset)].any()['Air Pollution Level'] and year + offset < 2025:
        election_result = row[party]
        pollution_before = row['Air Pollution Level']
        pollution_after = PM10_data[(PM10_data['Air Quality Station EoI Code'] == station) & (PM10_data['Year'] == year + offset)]['Air Pollution Level'].values[0]
        pollution_change = pollution_after - pollution_before
        x.append(election_result)
        y.append(pollution_change)

print(len(x))

x = np.array(x)
y = np.array(y)
res = stats.linregress(x, y)
plt.plot(x, y, 'o', label='original data')
plt.plot(x, res.intercept + res.slope*x, 'r', label='fitted line')
plt.legend()
plt.show()