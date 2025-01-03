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

parties = ['CDU', 'SPD', 'GRÜNE/B 90', 'GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'LÖS & GRÜNE/B90', 'FDP', 'AfD', 'DIE LINKE']

cities = [city + ', Stadt' for city in cities]

# 2024
data = pd.read_csv('DL_BB_GVW2024.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'in Prozent']]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['date'] = 2024
data['state'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)


data.to_csv('brandenburg.csv')


# 2019
data = pd.read_csv('DL_BB_GV2019.csv')
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'in Prozent']]
data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='in Prozent')
data['date'] = 2019
data['state'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']
data.index = data.index.str.replace(r', Stadt$', '', regex=True)

data.to_csv('brandenburg.csv', mode='a', header=False)

# 2014
cities = [city[:-7] for city in cities]

data = pd.read_csv('DL_BB_GV2014.csv')

data['Gemeindename'] = data['Gemeindename'].str.rstrip()
print(data)
data = data[data['Gemeindename'].isin(cities)]
data = data[data['Kurzname'].isin(parties)]
data = data.loc[:, ['Gemeindename' , 'Kurzname', 'Sitze']]
print(data)

data = data.replace(['GRÜNE/B 90 & BI Stadtentwicklung', 'GRÜNE/B 90 - VEREINTE.WfLU', 'GRÜNE/B 90', 'LÖS & GRÜNE/B90'], 'Gruene')

data = data.pivot(index='Gemeindename', columns='Kurzname', values='Sitze')
data['date'] = 2019
data['state'] = 'BB'
data = data.rename(columns={'DIE LINKE': 'Linke'}, index={'Gemeindename': 'City'})
data.index.names = ['City']

print(data)
