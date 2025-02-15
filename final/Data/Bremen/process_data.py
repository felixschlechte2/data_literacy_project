import csv

# Input and output file paths
input_files = ["Bremen_raw.csv"]
output_file = "Bremen.csv"


appearing_cities = []

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

        with open(input_files[0], mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile, delimiter=';')
            for row in reader:
                 new_row = [row[0],row[1],int(row[2]),int(row[3])/int(row[9])*100,int(row[4])/int(row[9])*100,
                            int(row[5])/int(row[9])*100,int(row[6])/int(row[9])*100,int(row[7])/int(row[9])*100,int(row[8])/int(row[9])*100]
                 new_row.append(100- sum(new_row[3:8]))
                 print(new_row)
                 writer.writerow(new_row)
        

