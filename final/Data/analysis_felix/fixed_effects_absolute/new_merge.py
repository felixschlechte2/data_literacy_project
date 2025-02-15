import pandas as pd

election_df_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\election_data.csv'
air_data_df_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10.csv'

merged_file = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10_and_elec.csv'
missing_rows = r'C:\Users\Home\Documents\M. Sc. ML\Data Literacy\analysis_felix\fixed_effects_absolute\PM10_and_elec_missing.csv'

air_df = pd.read_csv(air_data_df_file)
elec_df = pd.read_csv(election_df_file)

air_and_election_df = pd.merge(air_df, elec_df, left_on=['City', 'Year'], right_on=['City', 'Date'])

air_and_election_df.rename(columns={'Air Pollution Level': 'Air_Pollution_Level'}, inplace=True)

air_and_election_df.to_csv(merged_file, index=False)

# das erstellt csv mit allen rows in election_data die nicht gemergt werden konnten:
air_and_election_df = pd.merge(air_df, elec_df, left_on=['City', 'Year'], right_on=['City', 'Date'], how='outer', indicator=True)
missing_from_df1 = air_and_election_df[air_and_election_df['_merge'] == 'right_only']  # Present in df2 but not df1
missing_from_df1.to_csv(missing_rows, index=False)

# das printed die Häufigkeit der vorkommenden Jahre in dem gemergten file
#year_abundance = {}
#for index, row in air_and_election_df.iterrows():
#    if row['Year'] not in year_abundance:
#         year_abundance[row['Year']] = 1
#    else: year_abundance[row['Year']] += 1
#print(year_abundance)