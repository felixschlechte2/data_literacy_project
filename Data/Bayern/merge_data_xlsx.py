import pandas as pd
import os

# got this via cities_over_20k_bayern.py
cities_over_20k = {'München': '1.510.378', 
                   'Nürnberg': '526.091', 
                   'Augsburg': '303.150', 
                   'Regensburg': '159.465', 
                   'Ingolstadt': '142.308', 
                   'Fürth': '132.032', 
                   'Würzburg': '128.246', 
                   'Erlangen': '117.806', 
                   'Bamberg': '80.580', 
                   'Landshut': '75.272', 
                   'Bayreuth': '74.907', 
                   'Aschaffenburg': '72.918', 
                   'Kempten (Allgäu)': '70.713', 
                   'Rosenheim': '65.192', 
                   'Neu-Ulm': '61.780', 
                   'Schweinfurt': '55.067', 
                   'Passau': '54.401', 
                   'Freising': '49.939', 
                   'Straubing': '49.775', 
                   'Dachau': '48.337', 
                   'Hof': '46.963', 
                   'Memmingen': '46.178', 
                   'Kaufbeuren': '46.386', 
                   'Weiden in der Oberpfalz': '43.188', 
                   'Amberg': '42.676', 
                   'Ansbach': '42.311', 
                   'Coburg': '42.139', 
                   'Germering': '41.822', 
                   'Schwabach': '41.380', 
                   'Neumarkt in der Oberpfalz': '41.255', 
                   'Fürstenfeldbruck': '38.187', 
                   'Erding': '37.169', 
                   'Deggendorf': '35.757', 
                   'Forchheim': '33.610', 
                   'Neuburg an der Donau': '30.881', 
                   'Friedberg': '30.670', 
                   'Schwandorf': '30.239', 
                   'Landsberg am Lech': '29.739', 
                   'Unterschleißheim': '29.661', 
                   'Königsbrunn': '28.377', 
                   'Olching': '28.052', 
                   'Garmisch-Partenkirchen': '27.509', 
                   'Pfaffenhofen an der Ilm': '27.143', 
                   'Lauf an der Pegnitz': '26.413', 
                   'Zirndorf': '26.257', 
                   'Unterhaching': '26.079', 
                   'Lindau (Bodensee)': '26.155', 
                   'Kulmbach': '26.052', 
                   'Geretsried': '25.863', 
                   'Vaterstetten': '25.596', 
                   'Roth': '25.405', 
                   'Waldkraiburg': '24.604', 
                   'Herzogenaurach': '24.674', 
                   'Starnberg': '23.940', 
                   'Gersthofen': '23.492', 
                   'Weilheim in Oberbayern': '23.378', 
                   'Bad Kissingen': '23.245', 
                   'Kitzingen': '23.377', 
                   'Senden': '23.143', 
                   'Neusäß': '23.251', 
                   'Haar': '23.056', 
                   'Ottobrunn': '22.510', 
                   'Karlsfeld': '22.101', 
                   'Aichach': '22.222', 
                   'Sonthofen': '22.035', 
                   'Mühldorf am Inn': '21.860', 
                   'Günzburg': '21.865', 
                   'Puchheim': '21.410', 
                   'Gauting': '21.435', 
                   'Traunstein': '21.551', 
                   'Traunreut': '21.021', 
                   'Nördlingen': '21.053', 
                   'Dingolfing': '20.927', 
                   'Neufahrn bei Freising': '20.819', 
                   'Lichtenfels': '20.403'}
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
    "Others": []  
}

df_collect = pd.DataFrame(data) # df to collet the data

covered_cities = []

# folder_path = ".\Data Literacy\Baden-Württemberg\data"
error_folder_path = ".\Data Literacy\Baden-Württemberg\errors_merging.txt"

# Pfad zur Excel-Datei
file_path = r'.\Data Literacy\Bayern\data\14431-005r.xlsx'
folder_path = r'.\Data Literacy\Bayern\data'


# used this, to get the dictionary cities_w_name_index (It contains all the cities we want and the array [Name in the data files, index in the files])
# for 13 cities I had to do this by hand

# df_data = pd.read_excel(file_path, engine='openpyxl')
# second_column = df_data.iloc[:, 1]

# # before this, I made sure that every excel has the same ordering of the cities
# city_with_index = {}
# for city in cities_over_20k:
#     city_with_index[city] = []

# for city in cities_over_20k:
#     for n in range(len(second_column)):
#         c = str(second_column[n])
#         if (city in str(c)) and ('(Lkr)' not in str(c)) and ('b.' not in str(c)):
#             city_with_index[city].append(c)
#             city_with_index[city].append(n)

# i = 0
# for city in city_with_index:
#     if len(city_with_index[city]) != 2:
#         i += 1
#         print(city)
#         print(city_with_index[city])
#         print("-------------------------------------------------")
# print(f"number of problematic cities: {i}")
# print("-------------------------------------------------")
# print(city_with_index)

cities_w_name_index = {'München': ['    München, Landeshauptstadt', 8], 
                       'Nürnberg': ['    Nürnberg (Krfr.St)', 1282], 
                       'Augsburg': ['    Augsburg (Krfr.St)', 1827], 
                       'Regensburg': ['    Regensburg (Krfr.St)', 810], 
                       'Ingolstadt': ['    Ingolstadt (Krfr.St)', 7], 
                       'Fürth': ['    Fürth (Krfr.St)', 1281], 
                       'Würzburg': ['    Würzburg (Krfr.St)', 1504], 
                       'Erlangen': ['    Erlangen (Krfr.St)', 1280], 
                       'Bamberg': ['    Bamberg (Krfr.St)', 1048], 
                       'Landshut': ['    Landshut (Krfr.St)', 539], 
                       'Bayreuth': ['    Bayreuth (Krfr.St)', 1049], 
                       'Aschaffenburg': ['    Aschaffenburg (Krfr.St)', 1502], 
                       'Kempten (Allgäu)': ['    Kempten (Allgäu) (Krfr.St)', 1829], 
                       'Rosenheim': ['    Rosenheim (Krfr.St)', 9], 
                       'Neu-Ulm': ['      Neu-Ulm, GKSt', 1976], 
                       'Schweinfurt': ['    Schweinfurt (Krfr.St)', 1503], 
                       'Passau': ['    Passau (Krfr.St)', 540], 
                       'Freising': ['      Freising, GKSt', 182], 
                       'Straubing': ['    Straubing (Krfr.St)', 541], 
                       'Dachau': ['      Dachau, GKSt', 78], 
                       'Hof': ['    Hof (Krfr.St)', 1051], 
                       'Memmingen': ['    Memmingen (Krfr.St)', 1830], 
                       'Kaufbeuren': ['    Kaufbeuren (Krfr.St)', 1828], 
                       'Weiden in der Oberpfalz': ['    Weiden i.d.OPf. (Krfr.St)', 811], 
                       'Amberg': ['    Amberg (Krfr.St)', 809], 
                       'Ansbach': ['    Ansbach (Krfr.St)', 1279], 
                       'Coburg': ['    Coburg (Krfr.St)', 1050], 
                       'Germering': ['      Germering, GKSt', 208], 
                       'Schwabach': ['    Schwabach (Krfr.St)', 1283], 
                       'Neumarkt in der Oberpfalz': ['      Neumarkt i.d.OPf., GKSt', 893], 
                       'Fürstenfeldbruck': ['      Fürstenfeldbruck, GKSt', 207], 
                       'Erding': ['      Erding, GKSt', 154], 
                       'Deggendorf': ['      Deggendorf, GKSt', 548], 
                       'Forchheim': ['      Forchheim, GKSt', 1150], 
                       'Neuburg an der Donau': ['      Neuburg a.d.Donau, GKSt', 374], 
                       'Friedberg': ['      Friedberg, St', 1838], 
                       'Schwandorf': ['      Schwandorf, GKSt', 1004], 
                       'Landsberg am Lech': ['      Landsberg am Lech, GKSt', 264], 
                       'Unterschleißheim': ['      Unterschleißheim, St', 361], 
                       'Königsbrunn': ['      Königsbrunn, St', 1880], 
                       'Olching': ['      Olching, St', 220], 
                       'Garmisch-Partenkirchen': ['      Garmisch-Partenkirchen, M', 230], 
                       'Pfaffenhofen an der Ilm': ['      Pfaffenhofen a.d.Ilm, St', 393], 
                       'Lauf an der Pegnitz': ['      Lauf a.d.Pegnitz, St', 1397], 
                       'Zirndorf': ['      Zirndorf, St', 1385], 
                       'Unterhaching': ['      Unterhaching', 360], 
                       'Lindau (Bodensee)': ['      Lindau (Bodensee), GKSt', 1993], 
                       'Kulmbach': ['      Kulmbach, GKSt', 1230], 
                       'Geretsried': ['      Geretsried, St', 61], 
                       'Vaterstetten': ['      Vaterstetten', 109], 
                       'Roth': ['      Roth, St', 1468], 
                       'Waldkraiburg': ['      Waldkraiburg, St', 329], 
                       'Herzogenaurach': ['      Herzogenaurach, St', 1355], 
                       'Starnberg': ['      Starnberg, St', 461], 
                       'Gersthofen': ['      Gersthofen, St', 1871], 
                       'Weilheim in Oberbayern': ['      Weilheim i.OB, St', 534], 
                       'Bad Kissingen': ['      Bad Kissingen, GKSt', 1543], 
                       'Kitzingen': ['      Kitzingen, GKSt', 1643], 
                       'Senden': ['      Senden, St', 1982], 
                       'Neusäß': ['      Neusäß, St', 1889], 
                       'Haar': ['      Haar', 341], 
                       'Ottobrunn': ['      Ottobrunn', 349], 
                       'Karlsfeld': ['      Karlsfeld', 82], 
                       'Aichach': ['      Aichach, St', 1834], 
                       'Sonthofen': ['      Sonthofen, St', 2175], 
                       'Mühldorf am Inn': ['      Mühldorf a.Inn, St', 314], 
                       'Günzburg': ['      Günzburg, GKSt', 1945], 
                       'Puchheim': ['      Puchheim, St', 221], 
                       'Gauting': ['      Gauting', 454], 
                       'Traunstein': ['      Traunstein, GKSt', 495], 
                       'Traunreut': ['      Traunreut, St', 494], 
                       'Nördlingen': ['      Nördlingen, GKSt', 2139], 
                       'Dingolfing': ['      Dingolfing, St', 793], 
                       'Neufahrn bei Freising': ['      Neufahrn b.Freising', 195], 
                       'Lichtenfels': ['      Lichtenfels, St', 1251]}

# with this I controlled the dictionary cities_w_name_index to make sure that every name and index matches for all files

# for file_name in os.listdir(folder_path):
#     file_path_readout = os.path.join(folder_path, file_name)

#     # Excel-Datei in ein DataFrame laden
#     df_data = pd.read_excel(file_path_readout, engine='openpyxl')

#     # DataFrame anzeigen
#     first_column = df_data.iloc[:, 0]
#     second_column = df_data.iloc[:, 1]

#     for city in cities_w_name_index:
#         index = cities_w_name_index[city][1]
#         if str(second_column[index]) != str(cities_w_name_index[city][0]):
#             print(f"File: {file_name}")
#             print(f"Stadt: {city}")
#             print(f"im File: {str(second_column[index])}")
#             print(f"script: {str(cities_w_name_index[city][0])}")
#             print("-------------------------------------------------")

# print(len(cities_w_name_index))

def summe(Linke, Gruene, SPD, FDP, CDU, AfD):
    s = 0
    if isinstance(Linke, (int, float)): s+= Linke
    if isinstance(Gruene, (int, float)): s+= Gruene
    if isinstance(SPD, (int, float)): s+= SPD
    if isinstance(FDP, (int, float)): s+= FDP
    if isinstance(CDU, (int, float)): s+= CDU
    if isinstance(AfD, (int, float)): s+= AfD
    return s

def convert(all, input):
    if isinstance(input, (int, float)): return input / all
    else: return input

for file_name in os.listdir(folder_path):
    file_path_readout = os.path.join(folder_path, file_name)

    # Excel-Datei in ein DataFrame laden
    df_data = pd.read_excel(file_path_readout, engine='openpyxl')

    year = df_data.iloc[2, 0][-4:]

    for city in cities_w_name_index:
        index = cities_w_name_index[city][1]

        all_seats = df_data.iloc[index, 2]

        Linke = convert(all_seats, df_data.iloc[index,8])
        Gruene = convert(all_seats, df_data.iloc[index,5])
        SPD = convert(all_seats, df_data.iloc[index,4])
        FDP = convert(all_seats, df_data.iloc[index,6])
        CDU = convert(all_seats, df_data.iloc[index,3])
        AfD = convert(all_seats, df_data.iloc[index,7])
        Others = 1 - summe(Linke, Gruene, SPD, FDP, CDU, AfD)
        
        df_collect.loc[len(df_collect)] = [city, "BY", year, Linke, Gruene, SPD, FDP, CDU, AfD, Others]

csv_file_path = r".\Data Literacy\Bayern\bayern.csv"
df_collect.to_csv(csv_file_path, index=False, encoding="utf-8")
    

    