import csv
import os

def construct_csv(output_file, input_files):
    # Define the header for the output CSV file
    header = [
        "City",
        "State",
        "Date",
        "Linke",
        "Gruene",
        "SPD",
        "FDP",
        "CDU",
        "AfD",
        "Others",
    ]
    # Open the output file for writing
    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header row

        for input_file in input_files:
            with open(input_file, mode="r", encoding="utf-8") as infile:
                reader = csv.reader(infile)
                rows = [row for row in reader]  # Extract the single column

                for row in rows:
                    # Write the new row to the output file
                    writer.writerow(row)
            

# Example usage
input_files = ["NRW2020_Kreisfrei.csv", "NRW2020_Gemeinden.csv", "NRW2014_Kreisfrei.csv", "NRW2014_Gemeinden.csv", "NRW2009_Kreisfrei.csv", "NRW2009_Gemeinden.csv",
                "NRW2004_Kreisfrei.csv", "NRW2004_Gemeinden.csv", "NRW1999_Kreisfrei.csv", "NRW1999_Gemeinden.csv"]
output_file = "Nordrhein-Westfalen.csv"

# Ensure all input files exist
for input_file in input_files:
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist.")

# Generate the output CSV
construct_csv(output_file, input_files)

print(f"CSV file '{output_file}' has been created.")
