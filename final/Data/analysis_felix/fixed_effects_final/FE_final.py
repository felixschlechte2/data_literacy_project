import pandas as pd
import numpy as np
import matplotlib  as plt
from linearmodels.panel import PanelOLS

processed_file = r"C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_final\processed.csv"

def process_data(parties, pollutant, offset):
    election_data = pd.read_csv(r'.\Data Literacy\analysis_felix\fixed_effects_final\election_data.csv')
    pollutant_data = pd.read_csv(fr'.\Data Literacy\analysis_felix\fixed_effects_final\{pollutant}.csv')
    pollutant_data = pollutant_data[['Air Quality Station EoI Code', 'Year', 'Air Pollution Level', 'City', 'Air Quality Station Type']]
    pollutant_data = pollutant_data.groupby(['Air Quality Station EoI Code', 'Year', 'City', 'Air Quality Station Type'], as_index=False).mean()

    data = pd.merge(election_data, pollutant_data, left_on=['City', 'Date'], right_on=['City', 'Year'])

    data = data[['Air Quality Station EoI Code', 'Date', 'Air Pollution Level', 'City', 'Air Quality Station Type'] + parties]

    # data = data[data[party] != 0]
    data['Date'] = pd.to_numeric(data['Date'])
    data['Change'] = 'None'

    for index, row in data.iterrows():
        station = row['Air Quality Station EoI Code']
        year = row['Date']
        if pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)].any()['Air Pollution Level'] and year + offset < 2025:
            election_result = row[parties]
            pollution_before = row['Air Pollution Level']
            pollution_after = pollutant_data[(pollutant_data['Air Quality Station EoI Code'] == station) & (pollutant_data['Year'] == year + offset)]['Air Pollution Level'].values[0]
            pollution_change =  (pollution_after - pollution_before) # / pollution_before
            row['Change'] = pollution_change
            data.iloc[index] = row
    data = data[data['Change'] != 'None']
    data['Change'] = data['Change'].astype('float64')
    return data

parties = ['Linke','Gruene','SPD','FDP','CDU','AfD']

df = process_data(parties, 'PM10', 5)

df = df.sort_values(by=['Air Quality Station EoI Code', 'Date'])
# df = df[df['Date'] <= 2013]
df.to_csv(processed_file, index=False)

df = df.set_index(['Air Quality Station EoI Code', 'Date'])
mod = PanelOLS.from_formula(
    'Change ~ Linke + Gruene + SPD + FDP + CDU + AfD + EntityEffects + TimeEffects',
    df
)

res = mod.fit()
print(res.summary)