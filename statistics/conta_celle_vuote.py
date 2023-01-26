import os
import csv

folder_path = '../datasets/1_input'  # sostituire con il percorso della cartella

empty_cells = 0
total_cells = 0

for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                empty_cells += row.count('')
                total_cells += len(row)

print(empty_cells)
print(total_cells)
