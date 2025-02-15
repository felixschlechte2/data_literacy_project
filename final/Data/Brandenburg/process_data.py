import pandas as pd

cities = ['Potsdam', 
          'Cottbus', 
          'Brandenburg an der Havel',
          'Frankfurt (Oder)',
          'Oranienburg',
          'Falkensee',
          'Bernau bei Berlin',
          'Eberswalde',
          'Königs Wusterhausen',
          'Schwedt/Oder',
          'Fürstenwalde/Spree',
          'Neuruppin',
          'Ludwigsfelde',
          'Teltow',
          'Strausberg',
          'Hohen Neuendorf',
          'Werder (Havel)',
          'Hennigsdorf',
          'Rathenow',
          'Eisenhüttenstadt',
          'Senftenberg',
          'Zossen',
          'Spremberg',
          'Luckenwalde']

parties = ['CDU', 'CDU/ANW', 'SPD', 'GRÜNE/B 90', 'GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'LÖS & GRÜNE/B90', 'GRÜNE/B 90&BI Stadtentw.', 'FDP', 'AfD', 'DIE LINKE', 'PDS']

cities = [city + ', Stadt' for city in cities]

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

# 2024
data = pd.read_csv('Data/DL_BB_GVW2024.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties + ['Sitze'])]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Sitze']]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='Sitze')
data['Date'] = 2024
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)
data = data.reset_index()

data[party_cols] = data[party_cols].div(data['Sitze'], axis=0) * 100
data = data.drop(columns=['Sitze'])
data = data.fillna(0)
data = data[column_order]

data.to_csv('brandenburg.csv', index=False)


# 2019
data = pd.read_csv('Data/DL_BB_GV2019.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Sitze']]

data['total_seats'] = data.groupby('Gemeindename')['Sitze'].transform('sum')
data['in Prozent'] = (data['Sitze'] / data['total_seats']) * 100

data = data[data['Kurzname'].isin(parties)]

data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2019
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)
data = data.reset_index()
data = data[column_order]
data = data.fillna(0)


data.to_csv('brandenburg.csv', mode='a', header=False, index=False)

# 2014
cities = [city[:-7] for city in cities]

data = pd.read_csv('Data/DL_BB_GV2014.csv')

data['Gemeindename'] = data['Gemeindename'].str.rstrip()
data = data[data['Gemeindename'].isin(cities)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Sitze']]

data['total_seats'] = data.groupby('Gemeindename')['Sitze'].transform('sum')
data['in Prozent'] = (data['Sitze'] / data['total_seats']) * 100

data = data[data['Kurzname'].isin(parties)]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90', 'GRÜNE/B 90&BI Stadtentw.'], 'Gruene')
data = data.replace(['CDU/ANW'], 'CDU')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2014
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data = data.reset_index()
data = data[column_order]
data = data.fillna(0)

data.to_csv('brandenburg.csv', mode='a', header=False, index=False)


# 2003
data = pd.read_csv('Data/election_data_2003_formatted.csv')


data['Gemeindename'] = data['Gemeindename'].str.rstrip()
data['Kurzname'] = data['Kurzname'].str.rstrip()

data = data[data['Gemeindename'].isin(cities)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Sitze']]

data['total_seats'] = data.groupby('Gemeindename')['Sitze'].transform('sum')
data['in Prozent'] = (data['Sitze'] / data['total_seats']) * 100

data = data[data['Kurzname'].isin(parties)]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2003
data['State'] = 'BB'
data['AfD'] = 0
data = data.rename(columns={'PDS': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']

data = data.reset_index()
data = data[column_order]

data.to_csv('brandenburg.csv', mode='a', header=False, index=False)

# add others
party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

data = pd.read_csv('brandenburg.csv')

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors='coerce')
data['Others'] = 100 - data[party_cols].sum(axis=1)
data = data.fillna(0)

data.to_csv('brandenburg.csv', index=False)
