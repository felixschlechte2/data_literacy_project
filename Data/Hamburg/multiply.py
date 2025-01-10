import pandas as pd

file = r".\Data Literacy\Hamburg\hamburg.csv"

df = pd.read_csv(file, sep =";", encoding='latin1')

for zeile in df.index:
    for spalte in df.columns[3:]:
        wert = df.at[zeile, spalte]
        df.at[zeile, spalte] = 100*float(wert.replace(",", "."))

df.to_csv(file, sep=";", index=False)