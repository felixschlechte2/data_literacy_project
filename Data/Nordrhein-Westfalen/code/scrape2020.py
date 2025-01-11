from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from cities_over_20k import cities_over_20k
import pandas as pd
import time
import regex as re
import csv

error_file_path = "errors.txt"

rows = []

# Optionen für den Webdriver
#options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")

# Webdriver starten
#driver = webdriver.Chrome(options=options)

driver = webdriver.Firefox()


# Webseite laden
basic_url = "https://www.wahlergebnisse.nrw/kommunalwahlen/2020/index_obb_lr.shtml"  # Statistisches Landesamt BW
driver.get(basic_url)
def report_error(landkreis, gemeinde, e):
    with open(error_file_path, "a") as file:
        file.write(f"error for Landkreis number: {landkreis} and Gemeinde number: {gemeinde} \n")
        file.write("Fehler: \n")
        file.write(str(e))
        file.write("\n")
        file.write("_____________________________________________________________________ \n")

gemeinden = ["Düsseldorf","Duisburg","Essen","Krefeld","Mönchengladbach","Mülheim an der Ruhr","Oberhausen","Remscheid","Solingen","Wuppertal","Aachen","Bonn","Köln","Leverkusen",
             "Bottrop","Gelsenkirchen","Münster","Bielefeld","Bochum","Dortmund","Hagen","Hamm","Herne"]


for city in gemeinden:
    driver.get(basic_url)

    try:
        
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, city))  # Adjust the XPath as needed
        )
        button.click()


    except Exception as e:
        #report_error(city, None, e)
        print(f"problem with {city}")
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

        for j in range (9,55):
            try:
                
                text = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[1]").text
                
            except Exception as e: 
                continue    
            else:
                value = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[7]/* | //table/tbody/tr[{j}]/td[7]/b | //table/tbody/tr[{j}]/td[7]").text
                if "SPD" in text:
                    spd_value = value
                if "CDU" in text:
                    cdu_value = value
                if "GRÜNE" in text:
                    gruene_value = value
                if "FDP" in text:
                    fdp_value = value
                if "AfD" in text:
                    afd_value = value
                if "LINKE" in text:
                    linke_value = value

        summ = int(driver.find_element(By.XPATH, "/html/body/section[2]/div[2]/div[5]/div/table/tbody/tr[8]/td[7]").text)

        absolut = [linke_value, gruene_value, spd_value,fdp_value,cdu_value, afd_value]
        row = [int(a)/summ if '—' not in a else 0 for a in absolut]
        row.append(1 - sum([b for b in row]))
        row = [c*100 for c in row]
        row.append(city)
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
date = 2020

# Open the output file for writing
with open("NRW2020_Kreisfrei.csv", mode="w", newline="", encoding="utf-8") as outfile:
    writer = csv.writer(outfile)
    writer.writerow(header)  # Write the header row

    #counter = 0
    for i in rows:
        new_row = [i[7],
                "NRW",
                date]
        for count in range(0,7):
            new_row.append(i[count])
        print(new_row)
        # Write the new row to the output file
        writer.writerow(new_row)
        