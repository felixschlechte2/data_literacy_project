import os
import pandas as pd

# Define the folder path where the CSV files are stored
folder_path = "./raw"

# Initialize an empty DataFrame to collect unique rows
all_data = pd.DataFrame()

# Loop through all files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):  # Only process CSV files
        file_path = os.path.join(folder_path, file_name)
        # Read the CSV file
        df = pd.read_csv(file_path, usecols=["Air Quality Station EoI Code", "Longitude", "Latitude"])
        # Append to the main DataFrame
        all_data = pd.concat([all_data, df], ignore_index=True)

# Drop duplicate rows based on "Air Quality Station EoI Code"
unique_data = all_data.drop_duplicates(subset=["Air Quality Station EoI Code"])

# Save the unique rows to a new CSV file
output_file = "unique_air_quality_stations.csv"
unique_data.to_csv(output_file, index=False)

print(f"Unique rows saved to {output_file}")
