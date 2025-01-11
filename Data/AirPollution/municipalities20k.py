import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page
url = "https://en.wikipedia.org/wiki/List_of_municipalities_in_Germany"

# Fetch the webpage content
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table with municipalities
table = soup.find('table', {'class': 'wikitable'})

# Parse the table into a list of dictionaries
data = []
headers = [header.text.strip() for header in table.find_all('th')]

for row in table.find_all('tr')[1:]:
    cols = row.find_all('td')
    if len(cols) > 0:
        data.append({
            headers[i]: cols[i].text.strip() for i in range(len(cols))
        })

# Convert to DataFrame and save as CSV
df = pd.DataFrame(data)
df.to_csv('municipalities_germany.csv', index=False)

print("CSV file has been saved!")
