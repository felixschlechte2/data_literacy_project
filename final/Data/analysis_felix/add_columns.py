import pandas as pd

file = r'C:\Users\Home\Documents\M.Sc.ML\Data Literacy\analysis_felix\filled_elec.csv'

new_df = pd.read_csv(file)


for index, row in new_df.iterrows():
    if index % 1000 == 0: print(index)
    left = row['Linke'] + row['Gruene'] + row['SPD'] 
    right = row['FDP'] + row['CDU'] + row['AfD']
    new_df.at[index, 'left_coalition'] = left
    new_df.at[index, 'right_coalition'] = right
    new_df.at[index, 'left_dominated'] = (left > right)
    new_df.at[index, 'others_dominated'] = (row['Others'] > 50)


new_df.to_csv(file, index=False, encoding="utf-8")