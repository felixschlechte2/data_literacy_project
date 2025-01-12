import pandas as pd

cities = [
    r'Halle \(Saale\)',
    r'\bMagdeburg\b',
    r'Dessau-Ro[ß�]lau',
    r'Wittenberg',
    r'Halberstadt',
    r'Wei[ß�]enfels',
    r'Stendal',
    r'Bitterfeld-Wolfen',
    r'Merseburg',
    r'Naumburg \(Saale\)',
    r'Bernburg \(Saale\)',
    r'Wernigerode',
    r'Sch[ö�]nebeck \(Elbe\)',
    r'Zeitz',
    r'Aschersleben',
    r'Sangerhausen',
    r'K[ö�]then \(Anhalt\)',
    r'Sta[ß�]furt',
    r'Salzwedel',
    r'Quedlinburg',
    r'\bBurg\b',
    r'Eisleben',
    r'Gardelegen',
    r'Zerbst/Anhalt'
]

combined_cities = '(' + "|".join(cities) + ')'

parties = [r'CDU', r'DIE LINKE', r'SPD', r'AfD', r'GRÜNE', r'FDP']

combined_partys = "|".join(parties)

columns = '(' + '|'.join([r'Gültige Stimmen', r'Name', combined_partys]) + ')'

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

# 2024
data = pd.read_csv('Data/kw24dat3.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2024

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', index=False)


# 2019
data = pd.read_csv('Data/KW2019_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2019

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)


# 2014
data = pd.read_csv('Data/KW2014_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2014

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)


# 2009
data = pd.read_csv('Data/KW2009_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data['AfD'] = 0
data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2009

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)


#2007
parties_2007 = parties + [r'WASG']

combined_partys_2007 = "|".join(parties_2007)

columns_2007 = '(' + '|'.join([r'Gültige Stimmen', r'Name', combined_partys_2007]) + ')'

data = pd.read_csv('Data/KW2007_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns_2007)
data.columns = data.columns.str.extract(columns_2007)[0]

data['AfD'] = 0
data[parties_2007] = data[parties_2007].apply(pd.to_numeric, errors='coerce')
data['DIE LINKE'] = data[['DIE LINKE','WASG']].sum(axis=1)
data.drop('WASG', axis=1)
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2007

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)


# 2004
cities = cities + [r'Dessau']
combined_cities = '(' + "|".join(cities) + ')'

data = pd.read_csv('Data/KW2004_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data['AfD'] = 0
data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 2004

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)


# 1999
data = pd.read_csv('Data/KW1999_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data['AfD'] = 0
data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 1999

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)

# 1994
data = pd.read_csv('Data/KW1994_GEM.csv', sep=';', decimal=",")
data = data[data['Name'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data['AfD'] = 0
data[parties] = data[parties].apply(pd.to_numeric, errors='coerce')
data[parties] = data[parties].div(data['Gültige Stimmen'], axis=0) * 100

data = data.drop('Gültige Stimmen', axis=1)

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Name': 'City'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'SA'
data['Date'] = 1994

data = data[column_order]

data.to_csv('sachsen-anhalt.csv', mode='a', header=False, index=False)

# add others
party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']

data = pd.read_csv('sachsen-anhalt.csv')

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors='coerce')
data['Others'] = 100 - data[party_cols].sum(axis=1)
data = data.fillna(0)

data['City'] = data['City'].replace({
    'Dessau-Ro�lau': 'Dessau-Roßlau',
    'Wei�enfels': 'Weißenfels',
    'Sch�nebeck (Elbe)': 'Schönebeck (Elbe)',
    'K�then (Anhalt)': 'Köthen (Anhalt)',
    'Sta�furt': 'Staßfurt',
})


data.to_csv('sachsen-anhalt.csv', index=False)