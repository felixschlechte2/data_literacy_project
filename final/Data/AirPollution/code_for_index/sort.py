import csv

#result is a sorted csv file by name with the average molecule concentration in a city per year, i.e. city,year,average per row
with open("PM10.csv", mode="r", encoding="utf-8") as infile:
    reader = csv.reader(infile)
    header = next(reader)
    sorted_rows = sorted(reader, key=lambda row: row[9])
    city = sorted_rows[0][9]
    year_and_average = {}
    with open("PM10_sorted.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)

        for row in sorted_rows:
            if city != row[9]:
                for year in year_and_average:
                    writer.writerow([city,year,year_and_average[year][1]/year_and_average[year][0]])
                year_and_average = {}
                city = row[9]

            if row[2] not in year_and_average:
                if row[3] == '':
                    year_and_average[row[2]] = [1,0]
                else: 
                    year_and_average[row[2]] = [1,float(row[3])]
            else:
                if row[3] != '':
                    year_and_average[row[2]][0] += 1
                    year_and_average[row[2]][1] += float(row[3])
                    

    
     