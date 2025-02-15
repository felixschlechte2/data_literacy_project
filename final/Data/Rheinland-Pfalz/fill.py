import pandas as pd

data = {
    "City": [], 
    "State": [], 
    "Date": [],  
    "Linke": [],  
    "Gruene": [],  
    "SPD": [],  
    "FDP": [],  
    "CDU": [],  
    "AfD": [],  
    "Others": [],
    "gesamt": []  
}

df = pd.DataFrame(data) 

file_path = r'.\Data Literacy\Rheinland-Pfalz\rheinland-pfalz2.csv'

bezirke = ['Mainz', 'Ludwigshafen am Rhein', 'Koblenz', 'Trier', 'Kaiserslautern', 'Worms', 'Neuwied', 'Neustadt an der Weinstraße', 
           'Bad Kreuznach', 'Speyer', 'Frankenthal (Pfalz)', 'Landau in der Pfalz', 'Pirmasens', 'Ingelheim am Rhein', 
           'Zweibrücken', 'Andernach', 'Idar-Oberstein', 'Bad Neuenahr-Ahrweiler', 'Bingen am Rhein', 'Germersheim', 'Schifferstadt', 'Haßloch'] # Stand 31.12.23

jahre = [2024, 2019]

for b in bezirke:
    for j in jahre:
        df.loc[len(df)] = [b, "RP", j, '', '','','','','','','']

df.to_csv(file_path, index=False, encoding="utf-8")