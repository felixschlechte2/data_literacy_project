from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Optionen für den Webdriver
options = webdriver.ChromeOptions()
# options.add_argument("--start-maximized")

# Webdriver starten
driver = webdriver.Chrome(options=options)

# Webseite laden
url = r"https://de.wikipedia.org/wiki/Liste_der_gr%C3%B6%C3%9Ften_St%C3%A4dte_in_Bayern"  # Stand 31.12.2023
driver.get(url)

cities_over_20k = {}

# Wartezeit, um sicherzustellen, dass die Seite vollständig geladen ist
# time.sleep(3)

for rank in range(0,76):
    try:
        stadt = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{rank}]/td[2]/a')
        einwohner = driver.find_element(By.XPATH, f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{rank}]/td[6]')
        cities_over_20k[stadt.text] = einwohner.text

    except Exception as e:
        print("didnt work...")
        print(f"error for rank: {rank}")
        print("Fehler:", e)
        continue

driver.quit()

print(cities_over_20k)
print(len(cities_over_20k))

# https: // www.lambdatest.com / blog / handling - dropdown - in -selenium - webdriver - python /