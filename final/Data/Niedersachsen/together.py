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
    date = 2021
    # Open the output file for writing
    with open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        writer.writerow(header)  # Write the header row

        for input_file in input_files:
            with open(input_file, mode="r", encoding="utf-8") as infile:
                reader = csv.reader(infile)
                rows = [row for row in reader]  # Extract the single column

                # Ensure the input file has at least 8 rows for processing
                if len(rows) < 8:
                    print(f"Error: File {input_file} does not contain enough rows.")
                    continue
                
                for i in range(0,90):
                    row_inside = rows[i]

                    # Extract data from the rows
                    string = row_inside[0]
                    number7 = row_inside[7]
                    number3 = row_inside[3]
                    number2 = row_inside[2]
                    number4 = row_inside[4]
                    number1 = row_inside[1]
                    number6 = row_inside[6]
                    number5 = row_inside[5]
                    #print(rows[1])
                    # Construct the new row
                    new_row = [
                        string,
                        "NI",
                        date,
                        number7,
                        number3,
                        number2,
                        number4,
                        number1,
                        number6,
                        number5,
                    ]

                    # Write the new row to the output file
                    writer.writerow(new_row)
            date = date-5

# Example usage
input_files = ["Niedersachsen2021_Gemeinde.csv", "Niedersachsen2016_Gemeinde.csv", "Niedersachsen2011_Gemeinde.csv", "Niedersachsen2006_Gemeinde.csv", "Niedersachsen2001_Gemeinde.csv"]
output_file = "Niedersachsen.csv"

# Ensure all input files exist
for input_file in input_files:
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist.")

# Generate the output CSV
construct_csv(output_file, input_files)

print(f"CSV file '{output_file}' has been created.")
