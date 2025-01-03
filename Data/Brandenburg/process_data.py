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

# 2024
data = pd.read_csv('DL_BB_GVW2024.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'in Prozent']]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2024
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)
data = data.reset_index()
data = data[column_order]

data.to_csv('brandenburg.csv', index=False)


# 2019
data = pd.read_csv('DL_BB_GV2019.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'in Prozent']]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2019
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)
data = data.reset_index()
data = data[column_order]


data.to_csv('brandenburg.csv', mode='a', header=False, index=False)

# 2014
cities = [city[:-7] for city in cities]

data = pd.read_csv('DL_BB_GV2014.csv')

data['Gemeindename'] = data['Gemeindename'].str.rstrip()
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Stimmen']]

data['total_votes'] = data.groupby('Gemeindename')['Stimmen'].transform('sum')

data['in Prozent'] = (data['Stimmen'] / data['total_votes']) * 100

data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90', 'GRÜNE/B 90&BI Stadtentw.'], 'Gruene')
data = data.replace(['CDU/ANW'], 'CDU')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2014
data['State'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data = data.reset_index()
data = data[column_order]

data.to_csv('brandenburg.csv', mode='a', header=False, index=False)


# 2003
data = pd.read_csv('election_data_2003_formatted.csv')


data['Gemeindename'] = data['Gemeindename'].str.rstrip()
data['Kurzname'] = data['Kurzname'].str.rstrip()

data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Stimmen']]

print(data)

data['total_votes'] = data.groupby('Gemeindename')['Stimmen'].transform('sum')

data['in Prozent'] = (data['Stimmen'] / data['total_votes']) * 100

data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['Date'] = 2003
data['State'] = 'BB'
data['AfD'] = 0
data = data.rename(columns={'PDS': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']

data = data.reset_index()
data = data[column_order]
print(data)

data.to_csv('brandenburg.csv', mode='a', header=False, index=False)
