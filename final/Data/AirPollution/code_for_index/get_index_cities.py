import csv

def read_city_year_pairs(filename):
    with open(filename, mode='r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        return set((row[0], row[1]) for row in reader)
    

# assumes sorted_files
# result = list([city, year])
def german_AQI_cities_years(NO2, PM10, O3):
    pairs1 = read_city_year_pairs(NO2)
    pairs2 = read_city_year_pairs(PM10)
    pairs3 = read_city_year_pairs(O3)
    common_pairs = pairs1 & pairs2 & pairs3

    result = [[city, year] for city, year in common_pairs]
    return result

# assumes sorted_files
# result = list([city, year])
def vienna_AQI_cities_years(NO2, PM10, O3, SO2, CO):
    pairs1 = read_city_year_pairs(NO2)
    pairs2 = read_city_year_pairs(PM10)
    pairs3 = read_city_year_pairs(O3)
    pairs4 = read_city_year_pairs(SO2)
    pairs5 = read_city_year_pairs(CO)

    common_pairs = pairs1 & pairs2 & pairs3 & pairs4  &pairs5

    result = [[city, year] for city, year in common_pairs]
    return result

# assumes sorted_files
# result = list([city, year])
def BW_AQI_cities_years(NO2, PM10, O3, SO2, CO):
    pairs1 = read_city_year_pairs(NO2)
    pairs2 = read_city_year_pairs(PM10)
    pairs3 = read_city_year_pairs(O3)
    pairs4 = read_city_year_pairs(SO2)
    pairs5 = read_city_year_pairs(CO)

    common_pairs = pairs1 & pairs2 & pairs3 & pairs4  &pairs5

    result = [[city, year] for city, year in common_pairs]
    return result