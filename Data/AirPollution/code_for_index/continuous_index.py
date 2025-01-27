import csv
import os
import get_index_cities as gic

# returns list of individual molecule per city and year
def level(molecule_csv,pairs,):
    level = []
    with open(molecule_csv, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)

            for row in reader:
                if row[0:2] in pairs:
                    level.append(row[2])
            level = [float(level_indiv) if level_indiv != '' else 0 for level_indiv in level]
    return level


# returns lists of (city,year) and the individual lists of the molecules depending on the index one wants to use
def get_levels(NO2, PM10, O3):
    pairs = gic.german_AQI_cities_years(NO2, PM10, O3)

    NO2_levels = level(NO2,pairs)
    PM10_levels = level(PM10,pairs)
    O3_levels = level(O3,pairs)
        
    return pairs, NO2_levels, PM10_levels, O3_levels

# creates csv file with (city,year,index). For index: 1 is the best, 5 the worst
def german_AQI(NO2, PM10, O3):
    cities_years, NO2_levels, PM10_levels, O3_levels = get_levels(NO2, PM10, O3)
    rating = []
    for i in range(0,len(cities_years)):
        cities_years[i].append(min(1,max(NO2_levels[i]/201, O3_levels[i]/241, PM10_levels[i]/101)))
        rating.append(cities_years[i])
        #if cities_years[i][2] >0.7:
        #    print(cities_years[i])
        #    print(NO2_levels[i],O3_levels[i],PM10_levels[i])
        #    print("-----------------")

    with open("continuous_german_index.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for i in range(0,len(cities_years)):
            writer.writerow(rating[i]) 
    return rating


german_AQI("NO2_sorted.csv", "PM10_sorted.csv", "O3_sorted.csv")

print(f"CSV file has been created.")
