import os
import pandas as pd
import re
import csv

folder_path = ".\Data Literacy\Baden-Württemberg\data_2024"
error_folder_path = ".\Data Literacy\Baden-Württemberg\errors_merging.txt"

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

df = pd.DataFrame(data)

i = 0
# max_i = 4

def matching(m, content, all):
    if m == 'gesamt':
        match = re.search(r"Gewählte Gemeinderäte insgesamt\s*;(\d+);", content)
        if match:
            elem = int(match.group(1))
        else: 
            match2 = re.search(r"Gewählte Mitglieder insgesamt;(\d+);", content)
            if match2:
                elem = int(match2.group(1))
    elif m == 'linke':
        match = re.search(r"DIE LINKE;(x|-|[\d,]+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else: elem = '-'
    elif m == 'gruene':
        match = re.search(r"GRÜNE;(x|-|[\d,]+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else: elem = '-'
    elif m == 'spd':
        match = re.search(r"SPD;(x|-|\d+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else: elem = '-'
    elif m == 'fdp':
        match = re.search(r"FDP;(x|-|\d+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else:
            match2 = re.search(r"FDP/DVP;(x|-|\d+);", content)
            if match2:
                value = match2.group(1)  # Extrahiertes Zeichen oder Zahl
                if value == "-":
                    elem = "-"  # Speichere das Bindestrich-Zeichen
                else:
                    elem = float(value.replace(",", "."))/all
            else: elem = '-'
    elif m == 'cdu':
        match = re.search(r"CDU;(x|-|\d+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else: elem = '-'
    elif m == 'afd':
        match = re.search(r"AfD;(x|-|\d+);", content)
        if match:
            value = match.group(1)  # Extrahiertes Zeichen oder Zahl
            if value == "-":
                elem = "-"  # Speichere das Bindestrich-Zeichen
            else:
                elem = float(value.replace(",", "."))/all
        else: elem = '-'
    return elem

def summe(Linke, Gruene, SPD, FDP, CDU, AfD):
    s = 0
    if isinstance(Linke, (int, float)): s+= Linke
    if isinstance(Gruene, (int, float)): s+= Gruene
    if isinstance(SPD, (int, float)): s+= SPD
    if isinstance(FDP, (int, float)): s+= FDP
    if isinstance(CDU, (int, float)): s+= CDU
    if isinstance(AfD, (int, float)): s+= AfD
    return s

for file_name in os.listdir(folder_path):
    i += 1
    if (i % 10 == 0): print(f"i: {i}")
    file_path = os.path.join(folder_path, file_name)

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for _ in range(30):
                f.readline()
            second_line = f.readline()
            words = second_line.split()  # Zerlegt die Zeile in Wörter
            if words and "tadt" in words[0]:
                words.pop(0)
            city = " ".join(words)

            content = f.read()

            elected_all = matching('gesamt', content, None)
            Linke = matching('linke', content, elected_all)
            Gruene = matching('gruene', content, elected_all)
            SPD = matching('spd', content, elected_all)
            FDP = matching('fdp', content, elected_all)
            CDU = matching('cdu', content, elected_all)
            AfD = matching('afd', content, elected_all)
            Others = 1 - summe(Linke, Gruene, SPD, FDP, CDU, AfD)

        df.loc[len(df)] = [city, "BW", 2024, Linke, Gruene, SPD, FDP, CDU, AfD, Others]
    
    except Exception as e:
        with open(error_folder_path, "a") as file:
            file.write(f"error for file: {file_name} \n")
            file.write("Fehler: \n")
            file.write(str(e))
            file.write("\n")
            file.write("_____________________________________________________________________ \n")
        continue


######################################################################################################
# test which city are spelled different than in the years before:
# csv_file_path = r".\Data Literacy\Baden-Württemberg\baden-württemberg.csv"

# # Öffne die CSV-Datei
# with open(csv_file_path, "r", encoding="utf-8") as f:
#     reader = csv.reader(f)
    
#     # Zugriff auf die erste Spalte
#     first_column = [row[0] for row in reader]  # row[0] entspricht der ersten Spalte
#     for city in df["City"]:
#         if city not in first_column:
#             print(city)
######################################################################################################

csv_file_path = r".\Data Literacy\Baden-Württemberg\baden-württemberg.csv"
df.to_csv(csv_file_path, mode='a', index=False, header=False, encoding="utf-8")