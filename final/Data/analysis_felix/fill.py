import pandas as pd

election_df_file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\election_data.csv'
filled_elec_file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\filled_elec.csv'
just_sorted = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\just_sorted.csv'

df = pd.read_csv(election_df_file)

df_sorted = df.sort_values(by=["City", "Date"])

df_sorted.to_csv(just_sorted, index=False, encoding="utf-8")

empty1 = {}
new_df = pd.DataFrame(empty1)

for idx, (index, row) in enumerate(df_sorted.iterrows()):
    if idx % 100 == 0: print(idx)
    if idx + 1 < len(df_sorted):
        next_row = df_sorted.iloc[idx + 1]
    else:
        break

    if row['City'] == next_row['City']:
        missing_years = [row['Date']]
        for i in range(next_row['Date']- row['Date'] - 1):
            missing_years.append(row['Date'] + i + 1)
        empty = {
            'City': [], 
            'State': [],
            'Date': [],
            'Linke': [],
            'Gruene': [],
            'SPD': [],
            'FDP': [],
            'CDU': [],
            'AfD': [],
            'Others': []
        }
        for year in missing_years:
            empty['City'].append(row['City'])
            empty['State'].append(row['State'])
            empty['Date'].append(year)
            empty['Linke'].append(row['Linke'])
            empty['Gruene'].append(row['Gruene'])
            empty['SPD'].append(row['SPD'])
            empty['FDP'].append(row['FDP'])
            empty['CDU'].append(row['CDU'])
            empty['AfD'].append(row['AfD'])
            empty['Others'].append(row['Others'])
        df_fill = pd.DataFrame(empty)
        new_df = pd.concat([new_df, df_fill])
    else: continue

new_df['left_coalition'] = ''
new_df['right_coalition'] = ''
new_df['left_dominated'] = ''
new_df['others_dominated'] = ''

new_df.to_csv(filled_elec_file, index=False, encoding="utf-8")