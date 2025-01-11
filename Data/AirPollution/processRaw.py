import os
import pandas as pd

# Load the station code with location data
stations_with_location = pd.read_csv('stations_with_location.csv')

# Input and output directories
input_folder = './raw'
output_folder = './processed'

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # Read the current file
        input_file_path = os.path.join(input_folder, filename)
        current_df = pd.read_csv(input_file_path)

        # Merge with station location data based on station code
        merged_df = pd.merge(current_df, stations_with_location, how='left', on='Air Quality Station EoI Code')

        # Save the result to the output folder with the same filename
        output_file_path = os.path.join(output_folder, filename)
        merged_df.to_csv(output_file_path, index=False)

        print(f"Processed {filename} and saved to {output_file_path}")
