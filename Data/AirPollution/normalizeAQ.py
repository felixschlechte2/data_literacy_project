import pandas as pd
import os

# Input and output directories
input_folder = './filtered'
output_folder = './normalized'

def normalize_pollution_levels(input_csv, output_csv):
    # Read the CSV file
    df = pd.read_csv(input_csv)

    # Ensure the Air Pollution Level column is numeric
    df['Air Pollution Level'] = pd.to_numeric(df['Air Pollution Level'], errors='coerce')

    # Drop completely empty rows and rows missing critical values
    df = df.dropna(how='all')
    df = df.dropna(subset=['Year', 'Air Pollution Level'])

    # Group by year and normalize within each year
    def normalize_group(group):
        min_level = group['Air Pollution Level'].min()
        max_level = group['Air Pollution Level'].max()
        group['Normalized Pollution Level'] = (group['Air Pollution Level'] - min_level) / (max_level - min_level)
        return group

    # Use group_keys=False to avoid including group keys in the result
    df = df.groupby('Year', group_keys=False).apply(normalize_group)

    # Save the result to a new CSV file
    df.to_csv(output_csv, index=False)

    print(f"Normalized data saved to {output_csv}")

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.csv'):
        # Read the current file
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, filename)
        normalize_pollution_levels(input_file_path, output_file_path)
