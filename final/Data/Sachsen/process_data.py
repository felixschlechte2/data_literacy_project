import pandas as pd

cities = [
    r'Leipzig',
    r'Dresden',
    r'Chemnitz',
    r'Zwickau',
    r'Plauen',
    r'Görlitz',
    r'Freiberg',
    r'Freital',
    r'Pirna',
    r'Bautzen',
    r'Radebeul',
    r'Hoyerswerda',
    r'Riesa',
    r'Meißen',
    r'Grimma',
    r'Delitzsch',
    r'Zittau',
    r'Markkleeberg',
    r'Limbach-Oberfrohna',
    r'Döbeln',
    r'Glauchau',
    r'Werdau',
    r'Coswig',
    r'Reichenbach im Vogtland',
    r'Borna']

combined_cities = '(' + "|".join(cities) + ')'

column_order = ['City', 'State', 'Date', 'Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD', 'Others']

data = pd.read_csv('Data/SACHSEN2019.csv')

data = data[['Ortname', 'CDU in %', 'DIE LINKE in %', 'SPD in %', 'AfD in %', 'FDP in %', 'GRÜNE in %']]
data = data[data['Ortname'].str.contains(combined_cities)]

data = data.rename(columns={'Ortname': 'City', 'CDU in %': 'CDU', 'DIE LINKE in %': 'Linke', 'SPD in %': 'SPD', 'AfD in %': 'AfD', 'FDP in %': 'FDP', 'GRÜNE in %': 'Gruene'})
party_cols = ['Linke', 'Gruene', 'SPD', 'FDP', 'CDU', 'AfD']
data[party_cols] = data[party_cols].apply(pd.to_numeric, errors='coerce')
data['Others'] = (100 - data[party_cols].sum(axis=1)).clip(lower=0)
data['City'] = data['City'].str.extract(combined_cities)
data = data.fillna(0)

data['State'] = 'SN'
data['Date'] = 2019

data = data[column_order]

data.to_csv('sachsen.csv', index=False)
