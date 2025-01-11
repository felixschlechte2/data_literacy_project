from selenium import webdriver
from selenium.webdriver.common.by import By
# from cities_over_20k import cities_over_20k
import pandas as pd
import time
import regex as re
import csv

covered_cities = []
error_file_path = "errors.txt"

rows = []

# Optionen für den Webdriver
#options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")

# Webdriver starten
#driver = webdriver.Chrome(options=options)
driver = webdriver.Firefox()

# Webseite laden
basic_url = "http://alt.wahlergebnisse.nrw.de/kommunalwahlen/1999/raete_kreistag_krfrstaedte/"  # Statistisches Landesamt BW

def report_error(landkreis, gemeinde, e):
    with open(error_file_path, "a") as file:
        file.write(f"error for Landkreis number: {landkreis} and Gemeinde number: {gemeinde} \n")
        file.write("Fehler: \n")
        file.write(str(e))
        file.write("\n")
        file.write("_____________________________________________________________________ \n")

number_gemeinde =[111,112,113,114,116,117,119,120,122,124,313,314,315,316,
                  512,513,515,711,911,913,914,914,916]

gemeinden = ["Düsseldorf","Duisburg","Essen","Krefeld","Mönchengladbach","Mülheim an der Ruhr","Oberhausen","Remscheid","Solingen","Wuppertal","Aachen","Bonn","Köln","Leverkusen",
             "Bottrop","Gelsenkirchen","Münster","Bielefeld","Bochum","Dortmund","Hagen","Hamm","Herne"]


for i in number_gemeinde:
    try:
        url = basic_url + f"a{i}kw00.htm"
        driver.get(url)
    except Exception as e:
        print(f"error with {gemeinden[i]}")
        break
    else:
        summ = 0
        linke_value = 0
        gruene_value = 0
        spd_value = 0
        fdp_value = 0
        cdu_value = 0
        afd_value = 0
        sonstige_value = 0

        for j in range (1,30):
            try:
                #text = driver.find_element(By.XPATH,f"/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[{j}]/td[1]").text
                text = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[1]").text
            except Exception as e: 
                continue    
            else:
                
                value = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[4]/* | //table/tbody/tr[{j}]/td[4]/b | //table/tbody/tr[{j}]/td[4]").text
                if text == "SPD":
                    spd_value = value
                if text == "CDU":
                    cdu_value = value
                if text == "GRÜNE":
                    gruene_value = value
                if text == "FDP":
                    fdp_value = value
                if text == "AFD":
                    afd_value = value
                if text == "PDS":
                    linke_value = value
                if text == "WASG":
                    linke_value += value

                if value != "-": 
                    summ = summ + int(value)  

        absolut = [linke_value, gruene_value, spd_value,fdp_value,cdu_value, afd_value]
        row = [int(a)/summ if a != "-" else 0 for a in absolut]
        row.append(1 - sum([b for b in row]))
        row = [c*100 for c in row]
        print(absolut)
        print(summ)
        print(row)
        print("---------------")
        rows.append(row)


driver.quit()

# Define the header for the output CSV file
header = [
    "City",
    "State",
    "Date",
    "Linke",
    "Gruene",
    "SPD",
    "FDP",
    "CDU",
    "AfD",
    "Others",
    ]
date = 1999
# Open the output file for writing
with open("NRW1999_Kreisfrei.csv", mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)  # Write the header row

    counter = 0
    for i in rows:
        new_row = [gemeinden[counter],
                "NRW",
                date]
        for thing in i:
            new_row.append(thing)
        print(new_row)
        # Write the new row to the output file
        writer.writerow(new_row)
        counter +=1
