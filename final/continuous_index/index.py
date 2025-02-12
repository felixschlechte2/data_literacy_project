import pandas as pd
import csv

# result is a sorted datafram of that particullary pollutant
def sorted_data_frames(pollutant):
    pollutant_row = []
    with open(f"{pollutant}.csv", mode="r", encoding="utf-8") as infile:
        reader = csv.reader(infile)
        header = next(reader)
        sorted_rows = sorted(reader, key=lambda row: row[11])
        city = sorted_rows[0][11]
        year_and_average = {}
        
        for row in sorted_rows:
            if city != row[11]:
                for year in year_and_average:
                    pollutant_row.append([city,int(year),year_and_average[year][1]/year_and_average[year][0]])
                year_and_average = {}
                city = row[11]

            if row[2] not in year_and_average:
                if row[3] == '':
                    year_and_average[row[2]] = [1,0]
                else: 
                    year_and_average[row[2]] = [1,float(row[3])]
            else:
                if row[3] != '':
                    year_and_average[row[2]][0] += 1
                    year_and_average[row[2]][1] += float(row[3])

    return pollutant_row

# create the continuous index
def continuous_index():
    data_PM25 = pd.DataFrame(sorted_data_frames("PM25"),columns = ['City','Year','Average_PM25'])
    data_PM10 = pd.DataFrame(sorted_data_frames("PM10"),columns = ['City','Year','Average_PM10'])
    data_NO2 = pd.DataFrame(sorted_data_frames("NO2"),columns = ['City','Year','Average_NO2'])
    data_O3 = pd.DataFrame(sorted_data_frames("O3"),columns = ['City','Year','Average_O3'])

    data1 = pd.merge(data_PM25, data_PM10, on=['City', 'Year'])
    data2 = pd.merge(data_NO2, data_O3, on=['City', 'Year'])
    data = pd.merge(data1, data2, on=['City', 'Year'])

    # continuous index
    data['Index'] = pd.concat([
        data['Average_PM25']/51,
        data['Average_PM10']/101,
        data['Average_NO2']/201,
        data['Average_O3']/241
    ], axis=1).max(axis=1)

    data['Index'] = data['Index'].clip(upper=1)

    data = data[['City','Year','Index']]
    data.to_csv("continuous_index.csv", index=False, encoding="utf-8")
    
continuous_index()






