import os
import csv

folder_path = '../datasets/1_input'  # sostituire con il percorso della cartella

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            num_columns = len(next(reader))
            print(f"{file_name},{num_columns}")
