from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_cities():
    driver = webdriver.Firefox()
    cities = []

    stadte_url = "https://www.citypopulation.de/de/germany/cities/nordrheinwestfalen/"
    driver.get(stadte_url)


    try:
        # Example: Locate and click the "No" button
        no_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[9]/div[2]/div[2]/div[3]/div[2]/button[2]/p"))  # Adjust the XPath as needed
        )
        no_button.click()
        print("Clicked the 'No' button.")
    except Exception as e:
        print(f"Could not find the 'No' button: {e}")

    try:
        # Example: Locate and click the "sort" button
        no_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/article/section[3]/table/thead/tr/th[6]/span[1]"))  # Adjust the XPath as needed
        )
        no_button.click()
        print("Clicked the 'sort' button.")
    except Exception as e:
        print(f"Could not find the 'No' button: {e}")    


    for i in range(1,209):
        print
        city = driver.find_element(By.XPATH, f"/html/body/article/section[3]/table/tbody/tr[{i}]/td[1]/a/span").text
        cities.append(city)

    print(cities)
    driver.quit()
    return cities