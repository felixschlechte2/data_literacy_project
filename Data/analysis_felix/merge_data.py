import pandas as pd

election_df_file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\election_data.csv'
air_data_df_file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\NO2.csv'
elect_NO2_file = r"C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\elec_NO2.csv"

error_file = r"C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\errors.txt"

error_index = 0
city_error = 0
old_error = 0
state_error = 0
number_error = 0
rest_error = 0
def report_error(index, city, year, e):
    global error_index, city_error, old_error, state_error, number_error, rest_error
    error_index += 1
    if e == "City not found!": city_error += 1
    elif e == "air pollution data too old!": old_error += 1
    elif e == "Something sus with state!": state_error += 1
    elif e == "Found a weird number of election data!": number_error += 1
    else: rest_error += 1
    with open(error_file, "a") as file:
        file.write(f"error for index: {index} / city: {city} / year: {year} \n")
        file.write("Fehler: \n")
        file.write(str(e))
        file.write("\n")
        file.write("_______________________________________________________________________________________ \n")

air_df = pd.read_csv(air_data_df_file)
elec_df = pd.read_csv(election_df_file)

air_df["Linke"] = ''
air_df["Gruene"] = ''
air_df["SPD"] = ''
air_df["FDP"] = ''
air_df["CDU"] = ''
air_df["AfD"] = ''
air_df["Others"] = ''
air_df["year_of_last_vote"] = ''

for index, row in air_df.iterrows():
    if index % 1000 == 0: print(index)
    try: 
        relevant_rows = elec_df[elec_df.iloc[:,0] == row['City']]
        if relevant_rows.empty: 
            report_error(index, row['City'], row['Year'], "City not found!")
            continue

        # determine who reigned in the year of te data point
        year = row['Year']                                  # year of air data point
        relevant_years = relevant_rows['Date'].to_list()
        oldest = min(relevant_years)                        # determine the oldest year for which we have election data
        if year < oldest:                                   # no data for this year
            report_error(index, row['City'], row['Year'], "air pollution data too old!")
            continue                          
        for j in range(year - oldest):                      # determine the year of the nearest vote (attention: maybe finds data too far in the past!!)
            if year in relevant_years: break
            year -= 1
        
        final = relevant_rows[relevant_rows['Date'] == year]

        if final['State'].iloc[0] != row['State']:
            report_error(index, row['City'], row['Year'], "Something sus with state!")
            continue
        if len(final) != 1:
            report_error(index, row['City'], row['Year'], "Found a weird number of election data!")
            continue

        air_df.at[index, 'Linke'] = final['Linke'].iloc[0]
        air_df.at[index, 'Gruene'] = final['Gruene'].iloc[0]
        air_df.at[index, 'SPD'] = final['SPD'].iloc[0]
        air_df.at[index, 'FDP'] = final['FDP'].iloc[0]
        air_df.at[index, 'CDU'] = final['CDU'].iloc[0]
        air_df.at[index, 'AfD'] = final['AfD'].iloc[0]
        air_df.at[index, 'Others'] = final['Others'].iloc[0]
        air_df.at[index, 'year_of_last_vote'] = final['Date'].iloc[0]
    except Exception as e:
        report_error(index, row['City'], row['Year'], str(e))
        continue

air_df = air_df.sort_values(by=["City", "Year"]) 

air_df.to_csv(elect_NO2_file, index=False, encoding="utf-8")

with open(error_file, "a") as file:
        file.write("######################################################################################################### \n")
        file.write(f"errors in total: {error_index} - that's {error_index * 100/19812} % \n")
        file.write(f"   ->  city not found: {city_error} - that's {city_error * 100/19812} %\n")
        file.write(f"   ->  air data too old: {old_error} - that's {old_error * 100/19812} %\n")
        file.write(f"   ->  something sus with state: {state_error} - that's {state_error * 100/19812} %\n")
        file.write(f"   ->  found a weird number of election data: {number_error} - that's {number_error * 100/19812} %\n")
        file.write(f"   ->  rest: {rest_error} - that's {rest_error * 100/19812} %\n")
        file.write("######################################################################################################### \n")
