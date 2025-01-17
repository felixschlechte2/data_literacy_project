import pandas as pd
import os

# Load the station code with location data
stations_with_location = pd.read_csv('stations_with_location.csv')

# Input and output directories
input_folder = './processed'
output_folder = './filtered'




# Columns to select and their new names
columns_to_select = [
    "Air Quality Station EoI Code",
    "Air Pollutant",
    "Year",
    "Air Pollution Level",
    "Unit Of Air Pollution Level",
    "Air Quality Station Type",
    "Air Quality Station Area",
    "state",
    "district",
    "town_city"
]

# Column renaming mapping
renamed_columns = {
    "state": "State",
    "district": "District",
    "town_city": "City"
}

# State replacement mapping (from full names to abbreviations)
state_mapping = {
    "Baden-Württemberg": "BW",
    "Bayern": "BY",
    "Berlin": "BE",
    "Brandenburg": "BB",
    "Bremen": "HB",
    "Hamburg": "HH",
    "Hessen": "HE",
    "Mecklenburg-Vorpommern": "MV",
    "Niedersachsen": "NI",
    "Nordrhein-Westfalen": "NW",
    "Rheinland-Pfalz": "RP",
    "Saarland": "SL",
    "Sachsen": "SN",
    "Sachsen-Anhalt": "ST",
    "Schleswig-Holstein": "SH",
    "Thüringen": "TH"
}


# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # Read the current file
        input_file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(input_file_path)

        # Select and rename columns
        filtered_df = df[columns_to_select].rename(columns=renamed_columns)

        # Replace state values based on the mapping
        filtered_df["State"] = filtered_df["State"].replace(state_mapping)

        # Save the result to the output folder with the same filename
        output_file_path = os.path.join(output_folder, filename)
        filtered_df.to_csv(output_file_path, index=False)

        print(f"Processed {filename} and saved to {output_file_path}")



