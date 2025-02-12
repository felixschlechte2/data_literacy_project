import csv
import os
import pandas as pd
import get_index_cities as gic

# returns list of individual molecule per city and year
def level(molecule_csv,pairs):
    level = []
    with open(molecule_csv, mode="r", encoding="utf-8") as infile:
            reader = csv.reader(infile)
            header = next(reader)

            for row in reader:
                #if [row[0], row[1], row[3]] in pairs: # to include the station type
                if [row[0], row[1]] in pairs: # to NOT include the station type 
                    level.append(row[2])
            level = [float(level_indiv) if level_indiv != '' else 0 for level_indiv in level]
    return level


# returns lists of (city,year) and the individual lists of the molecules
def get_levels(NO2, PM10, O3,PM25):
    pairs = gic.german_AQI_cities_years(NO2, PM10, O3, PM25)

    NO2_levels = level(NO2,pairs)
    PM10_levels = level(PM10,pairs)
    O3_levels = level(O3,pairs)
    PM25_levels = level(PM25,pairs)
        
    return pairs, NO2_levels, PM10_levels, O3_levels, PM25_levels

# creates csv file with (city,year,index)
def german_AQI(NO2, PM10, O3,PM25):
    cities_years, NO2_levels, PM10_levels, O3_levels, PM25_levels = get_levels(NO2, PM10, O3, PM25)
    
    rating = []
    for i in range(0,len(cities_years)):
        cities_years[i].append(min(1,max(PM25_levels[i]/51,NO2_levels[i]/201, O3_levels[i]/241, PM10_levels[i]/101)))
        rating.append(cities_years[i])

    with open("continuous_german_index_not_finished.csv", mode="w", newline="", encoding="utf-8") as outfile:
        #header = ["City","Year","Air Quality Station Type","Index"] # to include the station type
        header = ["City","Year","Index"] # to NOT include the station type
        writer = csv.writer(outfile)
        writer.writerow(header) 
        df = pd.DataFrame(rating, columns=header)
        print(df)
        for i in range(0,len(cities_years)):
            writer.writerow(rating[i]) 

    df = pd.read_csv("continuous_german_index_not_finished.csv")

    df_sorted = df.sort_values(by=[df.columns[0],df.columns[1]])

    #df_sorted.to_csv("continuous_german_index_station.csv", index=False, encoding="utf-8") # to include the station type
    df_sorted.to_csv("continuous_german_index.csv", index=False, encoding="utf-8") # to NOT include the station type
    return rating


german_AQI("NO2_sorted.csv", "PM10_sorted.csv", "O3_sorted.csv", "PM25_sorted.csv")

print(f"CSV file has been created.")
