import pandas as pd

# Load the two CSV files
stations_df = pd.read_csv('stations_with_location.csv')
municipalities_df = pd.read_csv('municipalities_germany.csv')

# Merge based on the matching 'town_city' and 'city' columns
merged_df = pd.merge(stations_df, municipalities_df, how='inner', left_on='town_city', right_on='city')

# Select relevant columns and save the result
result_df = merged_df
merged_df.to_csv('stationsOver20kPop.csv', index=False)

print("CSV with stations and populations over 20k saved!")
