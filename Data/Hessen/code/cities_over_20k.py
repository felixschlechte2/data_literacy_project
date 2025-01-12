from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_cities():
    driver = webdriver.Firefox()
    cities = []

    stadte_url = "https://de.wikipedia.org/wiki/Liste_der_gr%C3%B6%C3%9Ften_St%C3%A4dte_in_Hessen"
    driver.get(stadte_url)

    try:
        # Example: Locate and click the "No" button
        no_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div/div/button/span/svg/line[2]"))  # Adjust the XPath as needed
        )
        no_button.click()
    except Exception as e:
        print("just wait")
        

    for i in range(1,60):
        city = driver.find_element(By.XPATH, f"/html/body/div[4]/div[3]/div[5]/div[1]/table/tbody/tr[{i}]/td[2]/a").text
        cities.append(city)
    driver.quit()
    return cities
