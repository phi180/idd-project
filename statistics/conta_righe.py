import pandas as pd
import os

path = "../datasets/1_input/"  # specificare il percorso della cartella
total_rows = 0

rows = []

for filename in os.listdir(path):
    if filename.endswith(".csv"):
        file_path = os.path.join(path, filename)
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        rows.append((filename, len(df)))
        total_rows += len(df)

with open('righe.csv', 'a') as fd:
    for row in rows:
        myCsvRow = row[0] + ',' + str(row[1]) + '\n'
        fd.write(myCsvRow)

print("Il numero totale di righe è:", total_rows)