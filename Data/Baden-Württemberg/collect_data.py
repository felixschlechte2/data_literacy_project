from selenium import webdriver
from selenium.webdriver.common.by import By
# from cities_over_20k import cities_over_20k
import pandas as pd
import time
import regex as re

covered_cities = []
error_file_path = ".\Data Literacy\Baden-Württemberg\errors.txt"

cities_over_20k = {'Stuttgart': '633.484', 
                    'Mannheim': '316.877', 
                    'Karlsruhe': '309.964', 
                    'Freiburg im Breisgau': '237.244', 
                    'Heidelberg': '162.960', 
                    'Heilbronn': '130.093', 
                    'Ulm': '129.942', 
                    'Pforzheim': '128.992', 
                    'Reutlingen': '118.528', 
                    'Esslingen am Neckar': '95.881', 
                    'Ludwigsburg': '94.859', 
                    'Tübingen': '93.615', 
                    'Villingen-Schwenningen': '89.145', 
                    'Konstanz': '85.770', 
                    'Aalen': '69.147', 
                    'Sindelfingen': '65.504', 
                    'Friedrichshafen': '63.441', 
                    'Schwäbisch Gmünd': '62.726', 
                    'Offenburg': '62.195', 
                    'Göppingen': '59.300', 
                    'Baden-Baden': '57.420', 
                    'Waiblingen': '55.917', 
                    'Böblingen': '52.093', 
                    'Rastatt': '51.800', 
                    'Ravensburg': '51.788', 
                    'Lörrach': '50.670', 
                    'Heidenheim an der Brenz': '49.895', 
                    'Leonberg': '49.845', 
                    'Singen (Hohentwiel)': '49.518', 
                    'Lahr/Schwarzwald': '49.420', 
                    'Bruchsal': '47.014', 
                    'Albstadt': '46.831', 
                    'Filderstadt': '46.295', 
                    'Fellbach': '46.205', 
                    'Weinheim': '45.381', 
                    'Rottenburg am Neckar': '44.791', 
                    'Bietigheim-Bissingen': '43.808', 
                    'Schwäbisch Hall': '42.743', 
                    'Kirchheim unter Teck': '42.178', 
                    'Nürtingen': '41.447', 
                    'Schorndorf': '40.614', 
                    'Leinfelden-Echterdingen': '40.526', 
                    'Ostfildern': '39.833', 
                    'Ettlingen': '39.763', 
                    'Kehl': '38.721', 
                    'Backnang': '38.184', 
                    'Tuttlingen': '37.784', 
                    'Sinsheim': '36.978', 
                    'Crailsheim': '36.239', 
                    'Balingen': '35.054', 
                    'Biberach an der Riß': '34.331', 
                    'Kornwestheim': '34.177', 
                    'Rheinfelden (Baden)': '33.849', 
                    'Herrenberg': '32.961', 
                    'Radolfzell am Bodensee': '32.575', 
                    'Weil am Rhein': '31.065', 
                    'Gaggenau': '30.190', 
                    'Bretten': '30.136', 
                    'Winnenden': '29.436', 
                    'Vaihingen an der Enz': '29.387', 
                    'Geislingen an der Steige': '29.261', 
                    'Bühl': '29.214', 
                    'Emmendingen': '29.035', 
                    'Wangen im Allgäu': '27.608', 
                    'Ehingen': '27.504', 
                    'Leimen': '27.286', 
                    'Weinstadt': '27.245', 
                    'Wiesloch': '27.120', 
                    'Achern': '26.664', 
                    'Mühlacker': '26.664', 
                    'Remseck am Neckar': '26.589', 
                    'Neckarsulm': '26.523', 
                    'Horb am Neckar': '25.695', 
                    'Öhringen': '25.591', 
                    'Rottweil': '25.548', 
                    'Weingarten': '25.521', 
                    'Ellwangen (Jagst)': '25.372', 
                    'Ditzingen': '25.318', 
                    'Stutensee': '25.311', 
                    'Waldshut-Tiengen': '25.114', 
                    'Bad Mergentheim': '24.752', 
                    'Calw': '24.448', 
                    'Freudenstadt': '24.337', 
                    'Mosbach': '23.647', 
                    'Leutkirch im Allgäu': '23.588', 
                    'Nagold': '23.321', 
                    'Wertheim': '23.319', 
                    'Überlingen': '23.240', 
                    'Laupheim': '23.044', 
                    'Bad Rappenau': '22.586', 
                    'Metzingen': '22.530', 
                    'Donaueschingen': '22.312', 
                    'Waldkirch': '22.266', 
                    'Eppingen': '22.252', 
                    'Bad Krozingen': '21.971', 
                    'Eislingen/Fils': '21.894', 
                    'Waghäusel': '21.766', 
                    'Hockenheim': '21.631', 
                    'Schwetzingen': '21.609', 
                    'Schramberg': '21.231', 
                    'Mössingen': '20.979', 
                    'Bad Waldsee': '20.786', 
                    'Rheinstetten': '20.695', 
                    'Korntal-Münchingen': '20.394', 
                    'Giengen an der Brenz': '20.358', 
                    'Tettnang': '20.262', 
                    'Schopfheim': '20.238', 
                    'Oberkirch': '20.237'}


# Optionen für den Webdriver
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Webdriver starten
driver = webdriver.Chrome(options=options)

# Webseite laden
url = "https://www.statistik-bw.de/SRDB/?H=Wahlen&U=Kommunal&T=02045036&E=GS"  # Statistisches Landesamt BW
driver.get(url)

def report_error(landkreis, gemeinde, e):
    with open(error_file_path, "a") as file:
        file.write(f"error for Landkreis number: {landkreis} and Gemeinde number: {gemeinde} \n")
        file.write("Fehler: \n")
        file.write(str(e))
        file.write("\n")
        file.write("_____________________________________________________________________ \n")


for landkreis in range(1,47): # 47
    try:
        driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[5]/option[{landkreis}]').click() # Landkreis Dropdown Menu
    except Exception as e:
        report_error(landkreis, None, e)
        continue
    else:
        # find number of Gemeinden:
        dropdown_list = driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[6]').text
        number_of_gemeinden = len(dropdown_list.splitlines()) + 1
        for gemeinde in range(2,number_of_gemeinden):
            try:
                driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[6]/option[{gemeinde}]').click() # Gemeinden Dropdown Menu
            except Exception as e:
                report_error(landkreis, gemeinde, e)
                continue
            else:
                text = driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[6]/option[{gemeinde}]').text
                city = text.split(',')[0]
                if city in cities_over_20k:
                    driver.find_element(By.XPATH, '//*[@id="SRDBform"]/div/input[1]').click() # 'Tabelle abrufen'
                    for year_counter in range(1,6):
                        driver.find_element(By.XPATH, f'//*[@id="figT-DB"]/table/thead/tr[1]/th/select/option[{year_counter}]').click()
                        try:
                            driver.find_element(By.XPATH, '//*[@id="asset-DB"]/ul/li/a').click()  # download csv - file
                            covered_cities.append(city)
                        except Exception as e:
                            report_error(landkreis, gemeinde, e)
                            continue
                    
                    # go back to original position:
                    driver.get(url)
                    driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[5]/option[{landkreis}]').click()
                    driver.find_element(By.XPATH, f'//*[@id="SRDBform"]/select[6]/option[{gemeinde}]').click()

driver.quit()