import pandas as pd

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD', 'Others']
party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

data = pd.read_csv('data.csv')
data[party_cols] = data[party_cols].apply(pd.to_numeric)
data['Others'] = data['Total'] - data[party_cols].sum(axis=1)
party_cols += ['Others']
data[party_cols] = data[party_cols].div(data['Total'], axis = 0) * 100
data['City'] = 'Berlin'
data['State'] = 'BE'

data = data[column_order]

data.to_csv('berlin.csv', index=False)