import pandas as pd

# Input and output file paths
input_file = './processed/PM10.csv'  # Replace with the path to your input CSV file
output_file = './filtered/PM10.csv'  # Replace with the desired output file name

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

# Read the input CSV
df = pd.read_csv(input_file)

# Select and rename columns
filtered_df = df[columns_to_select].rename(columns=renamed_columns)

# Replace state values based on the mapping
filtered_df["State"] = filtered_df["State"].replace(state_mapping)

# Save the filtered and updated data to a new CSV
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data with updated state abbreviations saved to {output_file}")
