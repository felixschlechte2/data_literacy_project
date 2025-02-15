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
def get_levels(NO2, PM10, O3, SO2, CO, name):

    if name == "german":
        pairs = gic.german_AQI_cities_years(NO2, PM10, O3)

        NO2_levels = level(NO2,pairs)
        PM10_levels = level(NO2,pairs)
        O3_levels = level(NO2,pairs)
        
        return pairs, NO2_levels, PM10_levels, O3_levels
    
    if name == "vienna" or name == "BW":
        pairs = gic.vienna_AQI_cities_years(NO2, PM10, O3, SO2, CO)

        NO2_levels = level(NO2,pairs)
        PM10_levels = level(PM10,pairs)
        O3_levels = level(O3,pairs)
        SO2_levels = level(SO2,pairs)
        CO_levels = level(CO,pairs)
        
        return pairs, NO2_levels, PM10_levels, O3_levels, SO2_levels, CO_levels
    else:
        return None

# creates csv file with (city,year,index). For index: 1 is the best, 5 the worst
def german_AQI(NO2, PM10, O3):
    cities_years, NO2_levels, PM10_levels, O3_levels = get_levels(NO2, PM10, O3, None, None, "german")
    rating = []
    for i in range(0,len(cities_years)):
        if NO2_levels[i] <= 20 and O3_levels[i] <= 60 and PM10_levels[i] <=20:
            cities_years[i].append(1)
        elif NO2_levels[i] <= 40 and O3_levels[i] <= 120 and PM10_levels[i] <=35:
            cities_years[i].append(2)
        elif NO2_levels[i] <= 100 and O3_levels[i] <= 180 and PM10_levels[i] <=50:
            cities_years[i].append(3)
        elif NO2_levels[i] <= 200 and O3_levels[i] <= 240 and PM10_levels[i] <100:
            cities_years[i].append(4)
        else: cities_years[i].append(5)
        rating.append(cities_years[i])
        #if cities_years[i][2] >4:
        #    print(cities_years[i])
        #    print(NO2_levels[i],O3_levels[i],PM10_levels[i])
        #    print("-----------------")

    with open("index_AQ_german.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for i in range(0,len(cities_years)):
            writer.writerow(rating[i]) 
    return rating

# different time frame for the levels  i.e. 1h average vs 8h average-> important??
# creates csv file with (city,year,index). For index: 1 is the best, 6 the worst
def vienna_AQI(NO2, PM10, O3, SO2, CO):
    cities_years, NO2_levels, PM10_levels, O3_levels, SO2_levels, CO_levels = get_levels(NO2, PM10, O3, SO2, CO, "vienna")
    rating = []
    for i in range(0,len(cities_years)):
        if NO2_levels[i] <= 45 and O3_levels[i] <= 60 and PM10_levels[i] <=20 and SO2_levels[i] <= 50 and CO_levels[i] <= 2.5:
            cities_years[i].append(1)
        elif NO2_levels[i] <= 100 and O3_levels[i] <= 90 and PM10_levels[i] <=35 and SO2_levels[i] <= 85 and CO_levels[i] <= 3.5:
            cities_years[i].append(2)
        elif NO2_levels[i] <= 140 and O3_levels[i] <= 130 and PM10_levels[i] <=50 and SO2_levels[i] <= 120 and CO_levels[i] <= 5:
            cities_years[i].append(3)
        elif NO2_levels[i] <= 200 and O3_levels[i] <= 180 and PM10_levels[i] <100 and SO2_levels[i] <= 200 and CO_levels[i] <= 10.5:
            cities_years[i].append(4)
        elif NO2_levels[i] <= 400 and O3_levels[i] <= 240 and PM10_levels[i] <150 and SO2_levels[i] <= 500 and CO_levels[i] <= 20.5:
            cities_years[i].append(5)
        else: cities_years[i].append(6)
        rating.append(cities_years[i])
        #if cities_years[i][2] >4:
        #    print(cities_years[i])
        #    print(NO2_levels[i],O3_levels[i],PM10_levels[i],SO2_levels[i],CO_levels[i])
        #    print("-----------------")
    with open("index_AQ_vienna.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for i in range(0,len(cities_years)):
            writer.writerow(rating[i]) 
    return rating


#same things as vienna
# creates csv file with (city,year,index). For index: 1 is the best, 6 the worst
def BW_AQI(NO2, PM10, O3, SO2, CO):
    cities_years, NO2_levels, PM10_levels, O3_levels, SO2_levels, CO_levels = get_levels(NO2, PM10, O3, SO2, CO, "vienna")
    rating = []
    #NOCH FALSCHE RANGE
    for i in range(0,len(cities_years)):
        if NO2_levels[i] <= 25 and O3_levels[i] <= 33 and PM10_levels[i] <=10 and SO2_levels[i] <= 25 and CO_levels[i] <= 1:
            cities_years[i].append(1)
        elif NO2_levels[i] <= 50 and O3_levels[i] <= 65 and PM10_levels[i] <=20 and SO2_levels[i] <= 50 and CO_levels[i] <= 2:
            cities_years[i].append(2)
        elif NO2_levels[i] <= 100 and O3_levels[i] <= 120 and PM10_levels[i] <=35 and SO2_levels[i] <= 120 and CO_levels[i] <= 4:
            cities_years[i].append(3)
        elif NO2_levels[i] <= 200 and O3_levels[i] <= 180 and PM10_levels[i] <50 and SO2_levels[i] <= 350 and CO_levels[i] <= 10:
            cities_years[i].append(4)
        elif NO2_levels[i] <= 500 and O3_levels[i] <= 240 and PM10_levels[i] <100 and SO2_levels[i] <= 1000 and CO_levels[i] <= 30:
            cities_years[i].append(5)
        else: cities_years[i].append(6)

        rating.append(cities_years[i])
        #if cities_years[i][2] >4:
        #    print(cities_years[i])
        #    print(NO2_levels[i],O3_levels[i],PM10_levels[i],SO2_levels[i],CO_levels[i])
        #    print("-----------------")
    with open("index_AQ_BW.csv", mode="w", newline="", encoding="utf-8") as outfile:
        writer = csv.writer(outfile)
        for i in range(0,len(cities_years)):
            writer.writerow(rating[i]) 
    return rating


german_AQI("NO2_sorted.csv", "PM10_sorted.csv", "O3_sorted.csv")
vienna_AQI("NO2_sorted.csv", "PM10_sorted.csv", "O3_sorted.csv", "SO2_sorted.csv", "CO_sorted.csv")
BW_AQI("NO2_sorted.csv", "PM10_sorted.csv", "O3_sorted.csv", "SO2_sorted.csv", "CO_sorted.csv")
    

print(f"CSV files have been created.")
