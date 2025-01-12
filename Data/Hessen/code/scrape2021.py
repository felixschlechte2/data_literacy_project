import csv
from cities_over_20k import get_cities
cities = get_cities()
print(cities)

def check_cities(city):
    if city in cities:
        return city
    j = 0
    for i in cities:
        if i in city:
            if i == "Fulda" and j != 1:
                j == 1
                continue
            return i
    
    n = len(city)
    
    for i in range(0,n-1):
        if city[i] == '�':
            if city[0:i]+ "ä"+ city[i+1:n] in cities:
                return city[0:i]+ "ä"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ä"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ö"+ city[i+1:n] in cities:
                return city[0:i]+ "ö"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ö"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ü"+ city[i+1:n] in cities:
                return city[0:i]+ "ü"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ü"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
            elif city[0:i]+ "ß"+ city[i+1:n] in cities:
                return city[0:i]+ "ß"+ city[i+1:n]
            elif any(substring in city[0:i]+ "ß"+ city[i+1:n] for substring in cities):
                for j in cities:
                    if j in city[0:i]+ "ß"+ city[i+1:n]:
                        return j
    return None



# Input and output file paths
input_csv_file = "2021_Gemeinden.csv"
output_csv_file = "HE2021.csv"

names = []
counter = 0

# Open the input CSV file for reading
with open(input_csv_file, 'r',encoding='utf-8', errors='replace') as infile, open(output_csv_file, 'w',encoding='utf-8', newline='') as outfile:
    reader = csv.reader(infile, delimiter=';')
    writer = csv.writer(outfile)

    # Process each row from the input file
    for line in reader:
        row = []
        summ = 0
        # Extract the desired values
        name_as_list = [line[2]]
        # Write in the output file
        name_as_list = [item.replace(", Stadt", "") for item in name_as_list]
        name_as_list = [item.replace(", Wissenschaftsstadt", "") for item in name_as_list]
        if check_cities(name_as_list[0]) != None:
            print(check_cities(name_as_list[0]))
            row.append(check_cities(name_as_list[0]))
        else: 
            print(name_as_list)
            continue
        row.append("HE")
        row.append("2021")
        print(line)
        for j in range(13,81):
            if j % 2 == 0:
                continue
            value = line[j]
            if j == 17:
                spd_value = value
            if j == 13:
                cdu_value = value
            if j == 15:
                gruene_value = value
            if j == 21:
                fdp_value = value
            if j == 19:
                afd_value = value
            if j == 23:
                linke_value = value
            
            if value != '':
                summ += int(value)

        value_str_list = [linke_value, gruene_value, spd_value, fdp_value, cdu_value, afd_value]
        value_list = [int(a)/summ*100 if a != ''  else 0 for a in value_str_list]
        #print(value_str_list)
        row = row + value_list
        print(value_list)
        print(row)
        print("------------------")
        if 100-sum(value_list)<1/summ:
            row.append(0)
        else:
            row.append(100-sum(value_list))
        #print(row)
        names.append(row[0])
        writer.writerow(row)

print([c if c not in names else None for c in cities])

print(f"Processed values written to {output_csv_file}")
