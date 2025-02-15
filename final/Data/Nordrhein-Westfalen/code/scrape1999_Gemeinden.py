from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# from cities_over_20k import cities_over_20k
import pandas as pd
import time
import regex as re
import csv
from cities_over_20k import get_cities

cities = get_cities()
#print(cities)

fcked_cities = []
error_file_path = "errors.txt"

rows = []

# Optionen für den Webdriver
#options = webdriver.ChromeOptions()
#options.add_argument("--start-maximized")

# Webdriver starten
#driver = webdriver.Chrome(options=options)

driver = webdriver.Firefox()


# Webseite laden
basic_url = "http://alt.wahlergebnisse.nrw.de/kommunalwahlen/1999/buergermeister_kreisang_gem/"  # Statistisches Landesamt BW
driver.get(basic_url)
def report_error(landkreis, gemeinde, e):
    with open(error_file_path, "a") as file:
        file.write(f"error for Landkreis number: {landkreis} and Gemeinde number: {gemeinde} \n")
        file.write("Fehler: \n")
        file.write(str(e))
        file.write("\n")
        file.write("_____________________________________________________________________ \n")

#number_gemeinde =[111,112,113,114,116,117,119,120,122,124,313,314,315,316,
#                  512,513,515,711,911,913,914,914,916]

gemeinden = ["Düsseldorf","Duisburg","Essen","Krefeld","Mönchengladbach","Mülheim an der Ruhr","Oberhausen","Remscheid","Solingen","Wuppertal","Aachen","Bonn","Köln","Leverkusen",
             "Bottrop","Gelsenkirchen","Münster","Bielefeld","Bochum","Dortmund","Hagen","Hamm","Herne"]

cities = [item for item in cities if item not in gemeinden]
cities = [item.replace("(Rheinland)", "") for item in cities]
cities = [item.replace(" am See", "") for item in cities]
cities = [item.replace(" am Rhein", "") for item in cities]
cities = [item.replace("/Ruhr", "") for item in cities]
cities = [item.replace("Bedburg", "Bedburg, Stadt") for item in cities]
print(cities)

for city in cities:
    driver.get(basic_url)
    
    #if "Emmerich" in city or "Ennepetal" in city or "Baesweiler" in city or "Heiligenhaus" in city:
    #    fcked_cities.append(city)
    #    continue
    #if "Selm" in city or "Salzkotten" in city or "Verl" in city or "Warstein" in city or "Bedburg" in city:
    #    fcked_cities.append(city)
    #    continue
    #if "Schmallenberg" in city or "Herdecke" in city or "Büren" in city:
    #    fcked_cities.append(city)
    #    continue
    try:
        #driver.find_element(By.NAME, "username")

        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, city))  # Adjust the XPath as needed
        )
        button.click()
        #link = driver.find_element(By.LINK_TEXT, city)
        #link.click()

    except Exception as e:
        #report_error(city, None, e)
        print(f"problem with {city}")
        break
        continue
    else:
        summ = 0
        linke_value = 0
        gruene_value = 0
        spd_value = 0
        fdp_value = 0
        cdu_value = 0
        afd_value = 0
        sonstige_value = 0

        for j in range (1,15):
            try:
                #text = driver.find_element(By.XPATH,f"/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[{j}]/td[1]").text
                text = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[1]").text
                
            except Exception as e: 
                continue    
            else:
                value = driver.find_element(By.XPATH,f"//table/tbody/tr[{j}]/td[2]/* | //table/tbody/tr[{j}]/td[2]/b | //table/tbody/tr[{j}]/td[2]").text
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

        #for j in range (1,15):
        #    try:
        #       text = driver.find_element(By.XPATH,f"/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[{j}]/td[2]/b").text
        #    except Exception as e:
        #        continue    
        #    else:
        #        if text != "-": 
        #            summ = summ + int(text) 
        #summ = int(driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[3]/table[2]/tbody/tr[1]/td[2]/b").text)
        #spd_value = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[1]/td[2]/b").text
        #cdu_value = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[2]/td[2]/b").text
        #gruene_value = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[3]/td[2]/b").text
        #fdp_value = driver.find_element(By.XPATH, "/html/body/div/div[4]/div[2]/div[3]/table/tbody/tr[4]/td[2]/b").text
        #linke_value = driver.find_element(By.XPATH, "/html/body/div[1]/div[4]/div[2]/div[3]/table[2]/tbody/tr[7]/td[2]/b").text
        #sonstige_value = sum - linke_value - gruene_value - spd_value - fdp_value - cdu_value - afd_value
        absolut = [linke_value, gruene_value, spd_value,fdp_value,cdu_value, afd_value]
        row = [int(a)/summ if a != "-" else 0 for a in absolut]
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
date = 1999
checked_cities = [item for item in cities if item not in fcked_cities]

# Open the output file for writing
with open("NRW1999_Gemeinden.csv", mode="w", newline="", encoding="utf-8") as outfile:
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
        #counter +=1