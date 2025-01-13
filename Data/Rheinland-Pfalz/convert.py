import pandas as pd

file = r".\Data Literacy\Rheinland-Pfalz\rheinland-pfalz2.csv"

df = pd.read_csv(file, encoding='latin1')

i = 0
for zeile in df.index:
    gesamt = float(df.iloc[zeile, -1])
    s = 0
    for spalte in df.columns[3:]:
        if df.at[zeile, spalte] != "-":
            wert = float(df.at[zeile, spalte])
            neu = (wert/gesamt)*100
            df.at[zeile, spalte] = neu
            s += neu
        else:
            df.at[zeile, spalte] = 100 - s
        i += 1

print(i)

df = df.iloc[:,:-1]

df.to_csv(file, index=False)