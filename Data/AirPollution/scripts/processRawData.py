import pandas as pd
import os

# Load the station code with location data
stations_with_location = pd.read_csv('./stations_with_location.csv')

# Input and output directories
input_folder = '../raw'
output_folder = '../processed'


# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Columns to select and their new names
columns_to_select = [
    "Air Quality Station EoI Code",
    "Air Pollutant",
    "Year",
    "Air Pollution Level",
    "Unit Of Air Pollution Level",
    "Air Quality Station Type",
    "Air Quality Station Area",
    "Longitude_x",
    "Latitude_x",
    "state",
    "district",
    "town_city"
]

# Column renaming mapping
renamed_columns = {
    "state": "State",
    "district": "District",
    "town_city": "City",
    "Longitude_x": "Longitude",
    "Latitude_x": "Latitude"
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
    "Sachsen-Anhalt": "SA",
    "Schleswig-Holstein": "SH",
    "Thüringen": "TH"
}

def normalize_pollution_levels(df, output_csv):


    # Ensure the Air Pollution Level column is numeric
    df['Air Pollution Level'] = pd.to_numeric(df['Air Pollution Level'], errors='coerce')

    # Drop completely empty rows and rows missing critical values
    # df1 = df[df.isna().any(axis=1)]
    # print(df1)
    # df = df.dropna(how='all')
    df = df.dropna(subset=['Year', 'Air Pollution Level'])

    # Group by year and normalize within each year
    def normalize_group(group):
        min_level = group['Air Pollution Level'].min()
        max_level = group['Air Pollution Level'].max()
        group['Normalized Pollution Level'] = (group['Air Pollution Level'] - min_level) / (max_level - min_level)
        return group

    # Use group_keys=False to avoid including group keys in the result
    df = df.groupby('Year', group_keys=False).apply(normalize_group)

    df = df.sort_values(by=['State','City', 'Year'])
    # Save the result to a new CSV file
    df.to_csv(output_csv, index=False)

    print(f"Normalized data saved to {output_csv}")

def normalize_by_yearly_mean(df, output_csv):

    # Ensure relevant columns are numeric
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
    df['Air Pollution Level'] = pd.to_numeric(df['Air Pollution Level'], errors='coerce')

    # Drop rows with NaN values in critical columns
    df = df.dropna(subset=['Year', 'Air Pollution Level', 'City'])

    # Sort values by City and Year for proper difference calculation
    df = df.sort_values(by=['City', 'Year'])

    # Calculate the year-over-year difference for each city
    df['Yearly Difference'] = df.groupby('City')['Air Pollution Level'].diff()

    # Compute the mean Yearly Difference for each year
    yearly_mean = df.groupby('Year')['Yearly Difference'].mean().reset_index()
    yearly_mean.rename(columns={'Yearly Difference': 'Yearly Mean Difference'}, inplace=True)

    # Merge the yearly mean back into the original DataFrame
    df = df.merge(yearly_mean, on='Year', how='left')

    # Normalize each city's yearly difference by the yearly mean
    df['Normalized Difference'] = df['Yearly Difference'] / df['Yearly Mean Difference']

    df = df.sort_values(by=['State','City', 'Year'])

    # Save the result to a new CSV file
    df.to_csv(output_csv, index=False)

    print(f"Normalized data saved to {output_csv}")

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # Read the current file
        input_file_path = os.path.join(input_folder, filename)
        df = pd.read_csv(input_file_path)
        print(stations_with_location.columns)
        merged_df = pd.merge(df, stations_with_location, how='left', on='Air Quality Station EoI Code')
        print(merged_df.columns)
        # Select and rename columns
        filtered_df = merged_df[columns_to_select].rename(columns=renamed_columns)

        # Replace state values based on the mapping
        filtered_df["State"] = filtered_df["State"].replace(state_mapping)
        
        # Save the result to the output folder with the same filename
        output_file_path = os.path.join(output_folder, filename)
        normalize_by_yearly_mean(filtered_df, output_file_path)
        

        print(f"Processed {filename} and saved to {output_file_path}")



