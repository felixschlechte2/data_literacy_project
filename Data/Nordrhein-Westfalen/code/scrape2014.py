import csv

gemeinden = ["Düsseldorf","Duisburg","Essen","Krefeld","Mönchengladbach","Mülheim an der Ruhr","Oberhausen","Remscheid","Solingen","Wuppertal","Aachen","Bonn","Köln","Leverkusen",
             "Bottrop","Gelsenkirchen","Münster","Bielefeld","Bochum","Dortmund","Hagen","Hamm","Herne"]


def check_gemeinden(city):
    if city in gemeinden:
        return city
    
    n = len(city)
    
    for i in range(0,n-1):
        if city[i] == '�':
            if city[0:i]+ "ä"+ city[i+1:n] in gemeinden:
                return city[0:i]+ "ä"+ city[i+1:n]
            elif city[0:i]+ "ö"+ city[i+1:n] in gemeinden:
                return city[0:i]+ "ö"+ city[i+1:n]
            elif city[0:i]+ "ü"+ city[i+1:n] in gemeinden:
                return city[0:i]+ "ü"+ city[i+1:n]
    return None 



# Input and output file paths
input_csv_file = "2014.csv"
output_csv_file = "NRW2014_Kreisfrei.csv"

# Indices to extract (adjusted for 0-based indexing)
indices_to_extract = [1, 2, 5, 8, 11, 14, 17, 53]

# Open the input CSV file for reading
with open(input_csv_file, 'r',encoding='utf-8', errors='replace') as infile, open(output_csv_file, 'w',encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # Process each row from the input file
    for line in reader:
        row = []
        # Extract the desired values
        extracted_values = [line[i] if i < len(line) else '' for i in indices_to_extract]
        # Write in the output file
        extracted_values = [item.replace("Krfr. Stadt ", "") for item in extracted_values]
        
        if check_gemeinden(extracted_values[0]) != None:
            row.append(check_gemeinden(extracted_values[0]))
        else: 
            print(extracted_values[0])
            continue
        for j in range(2,8):
            value = extracted_values[j]
            if value == '':
                row.append(0)
            else:
                row.append(int(extracted_values[j])/int(extracted_values[1])*100)
        if 100-sum(row[1:6])<1/int(extracted_values[1]):
            row.append(0)
        else:
            row.append(100-sum(row[1:6]))
        
        writer.writerow(row)

print(f"Processed values written to {output_csv_file}")
