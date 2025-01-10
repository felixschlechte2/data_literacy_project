import pandas as pd

file = r".\Data Literacy\Bayern\bayern.csv"

df = pd.read_csv(file)

for zeile in df.index:
    for spalte in df.columns[3:]:
        wert = df.at[zeile, spalte]
        if wert != '-':
            df.at[zeile, spalte] = 100*float(wert)

df.to_csv(file, index=False)