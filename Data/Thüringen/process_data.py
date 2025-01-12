import pandas as pd

cities = [
    r'Erfurt',
    r'Jena(?!l[ö�]bnitz)',
    r'Gera(?!tal)(?!berg)',
    r'Weimar',
    r'Gotha',
    r'Eisenach',
    r'Nordhausen',
    r'Ilmenau',
    r'M[ü�]hlhausen',
    r'(?<!\w\. )Suhl(?!-)',
    r'Altenburg',
    r'Saalfeld(?!er)',
    r'Arnstadt',
    r'Meiningen',
    r'Rudolstadt',
    r'Sonneberg',
    r'Bad Salzungen',
    r'Apolda',
    r'Sondershausen',
    r'Greiz',
    r'Leinefelde-Worbis']

combined_cities = '(' + "|".join(cities) + ')'

parties = [r'CDU', r'DIE LINKE', r'SPD', r'AfD', r'GRÜNE', r'FDP', r'Sonstige']

combined_partys = "|".join(parties)

columns = '(' + '|'.join([r'Zu vergebene Sitze', r'Gemeindename', combined_partys]) + ')'

party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD', 'Others']

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD', 'Others']

# 2024
data = pd.read_csv('TH2024_Sitze.csv')
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 2024

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', index=False)

# 2019
data = pd.read_csv('TH2019_Sitze.csv')
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 2019

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)


# 2014
data = pd.read_csv('TH2014_Sitze.csv')
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
party_cols = ['CDU', 'Linke', 'SPD', 'AfD', 'Gruene', 'FDP']
data[party_cols] = data[party_cols].apply(pd.to_numeric, errors='coerce')
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 2014

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])

data['Others'] = 100 - data[party_cols].sum(axis=1)
party_cols += ['Others']
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)

# 2009
data = pd.read_csv('TH2009_Sitze.csv')
data['AfD'] = 0
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 2009

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)

# 2004
data = pd.read_csv('TH2004_Sitze.csv')
data['AfD'] = 0
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 2004

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)

# 1999
data = pd.read_csv('TH1999_Sitze.csv')
data['AfD'] = 0
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 1999

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)


# 1994
data = pd.read_csv('TH1994_Sitze.csv')
data['AfD'] = 0
data = data[data['Gemeindename'].str.contains(combined_cities)]
data = data.filter(regex=columns)
data.columns = data.columns.str.extract(columns)[0]

data = data.rename(columns={'DIE LINKE': 'Linke', 'GRÜNE': 'Gruene', 'Gemeindename': 'City', 'Sonstige': 'Others', 'Zu vergebene Sitze': 'total'})
data['City'] = data['City'].str.extract(combined_cities)
data['State'] = 'TH'
data['Date'] = 1994

data[party_cols] = data[party_cols].apply(pd.to_numeric, errors = 'coerce')
data[party_cols] = data[party_cols].div(data['total'], axis=0) * 100
data = data.drop(columns=['total'])
data = data.fillna(0)

data = data[column_order]

data.to_csv('thueringen.csv', mode='a', header=False, index=False)