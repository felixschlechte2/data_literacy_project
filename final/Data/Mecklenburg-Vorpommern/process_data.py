import pandas as pd

cities = [
    r'Rostock',
    r'(?<!Alt\s)Schwerin(?!sburg)',
    r'Neubrandenburg',
    r'Greifswald',
    r'Stralsund',
    r'Wismar',
    r'G[�ü]strow(?!-Land)',
    r'Waren \(M[�ü]ritz\)',
    r'Neustrelitz(?!-Land)',
]
combined_cities = "(" + "|".join(cities) + ")"

parties = ['CDU', 'DIE LINKE', 'SPD', 'AfD', 'GRÜNE', 'FDP']

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

# 2024
data = pd.read_csv('Data/k_gemeinden_2024.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.replace(r',.*', '', regex=True)
data['State'] = 'MV'
data['Date'] = 2024

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', index=False)


# 2019
data = pd.read_csv('Data/kw2019k_gemeinden.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 2019

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# 2014

data = pd.read_csv('Data/K_Gemeinden_2014.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 2014

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# 2011
data = pd.read_csv('Data/K_Gemeinden_2011.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data['AfD'] = 0
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 2011

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# 2009
data = pd.read_csv('Data/K_Gemeinden_2011.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data['AfD'] = 0
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 2009

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# 2004
parties = ['CDU', 'PDS', 'SPD', 'AfD', 'GRÜNE', 'FDP']
data = pd.read_csv('Data/KW 2004 Gemeinden.csv', sep=';', decimal=",")
data = data[data['Gemeindename'].str.contains(combined_cities)]
data['AfD'] = 0
data = data.loc[:, ['Gemeindename'] + parties]
data = data.loc[1::2]

data = data.rename(columns={'PDS': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 2004

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# 1999
parties_plus = parties + ['C22', 'Stimmen gesamt'] # C22 is the field for Bü90, which are the greens
data = pd.read_csv('Data/B734G 1999 01.csv')
data = data[data['Gemeindename'].str.contains(combined_cities)]
data['AfD'] = 0
data = data.loc[:, ['Gemeindename'] + parties_plus]
data[parties_plus] = data[parties_plus].apply(pd.to_numeric, errors='coerce')
data['GRÜNE'] = data[['GRÜNE', 'C22']].sum(axis=1)
data = data.drop('C22', axis=1)
data[parties] = data[parties].div(data['Stimmen gesamt'], axis=0) * 100

data = data.rename(columns={'PDS': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 1999

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)


# 1994
parties_plus = parties + ['D31', 'Stimmen gesamt'] # C22 is the field for Bü90, which are the greens
data = pd.read_csv('Data/B734G 1994 01.csv')
data = data[data['Gemeindename'].str.contains(combined_cities)]
data['AfD'] = 0
data = data.loc[:, ['Gemeindename'] + parties_plus]
data[parties_plus] = data[parties_plus].apply(pd.to_numeric, errors='coerce')
data['GRÜNE'] = data[['GRÜNE', 'D31']].sum(axis=1)
data = data.drop('D31', axis=1)
data[parties] = data[parties].div(data['Stimmen gesamt'], axis=0) * 100

data = data.rename(columns={'PDS': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City'})
data['City'] = data['City'].str.extract(combined_cities)

data['State'] = 'MV'
data['Date'] = 1994

data = data[column_order]

data.to_csv('mecklenburg-vorpommern.csv', mode='a', index=False, header=False)

# add others
party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

data = pd.read_csv('mecklenburg-vorpommern.csv')

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors='coerce')
data['Others'] = 100 - data[party_cols].sum(axis=1)
data = data.fillna(0)

data['City'] = data['City'].replace({
    'Waren (M�ritz)': 'Waren (Müritz)',
    'G�strow': 'Güstrow',
})

data.to_csv('mecklenburg-vorpommern.csv', index=False)
