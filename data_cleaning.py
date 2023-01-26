import os
import csv
import re
import shutil
from itertools import zip_longest
import pandas as pd

datasets_directory = 'datasets/'
datasets_input_directory = datasets_directory + 'input/'
datasets_output_directory = datasets_directory + 'cleaned/'


# reads from a file the datasets to clean
def read_datasets_to_clean():
    to_clean = []
    with open('config/data_cleaning/datasets_to_clean.txt') as f:
        for line in f:
            to_clean.append(line)

    return to_clean


def get_prefix_suffix_length(column, has_header):
    index_2_tokens_prefix = {}
    index_2_tokens_suffix = {}

    if has_header:
        column = column[1:]

    for cell in column:
        tokens = cell.split()
        cell_length = len(tokens)
        for i in range(0, cell_length):
            if not i in index_2_tokens_prefix:
                index_2_tokens_prefix[i] = set({})
            if not i in index_2_tokens_suffix:
                index_2_tokens_suffix[i] = set({})

            token_prefix = str(tokens[i])
            token_suffix = str(tokens[cell_length-i-1])

            tokenset_prefix = index_2_tokens_prefix[i]
            tokenset_suffix = index_2_tokens_suffix[i]

            if not token_prefix == 'nan':
                tokenset_prefix.add(token_prefix)
            if not token_suffix == 'nan':
                tokenset_suffix.add(token_suffix)

    prefix_length = 0
    for index in index_2_tokens_prefix:
        if len(index_2_tokens_prefix[index]) == 1:
            prefix_length = prefix_length + 1
        else:
            break

    suffix_length = 0
    for index in index_2_tokens_suffix:
        if len(index_2_tokens_suffix[index]) == 1:
            suffix_length = suffix_length + 1
        else:
            break

    return prefix_length, suffix_length


# returns file names of csv datasets to be cleaned
def get_datasets(datasets_path):
    datasets = []

    for filename in os.listdir(datasets_path):
        f = os.path.join(datasets_path, filename)
        if os.path.isfile(f):
            datasets.append(filename)

    return datasets


def remove_special_chars(string):
    output = re.sub("[^A-Za-z0-9 ]", "", string)
    return output


def write_cleaned_columns_to_file(dataset_name, head, cleaned_columns):
    export_data = zip_longest(*cleaned_columns, fillvalue='')
    with open(os.path.join(datasets_output_directory, dataset_name), 'w', encoding="ISO-8859-1",
              newline='') as cleaned_dataset_file:
        wr = csv.writer(cleaned_dataset_file)
        wr.writerow(head)
        wr.writerows(export_data)
        cleaned_dataset_file.close()


def main():
    datasets_files = get_datasets(datasets_input_directory)

    for dataset_name in datasets_files:
        if dataset_name in read_datasets_to_clean():
            dataset_path = os.path.join(datasets_input_directory, dataset_name)
            df = pd.read_csv(dataset_path, dtype=str)
            df = df.astype(str)

            cleaned_columns = []
            for column in df:
                col_list = list(df[column])
                cleaned_column = [remove_special_chars(str(w)) for w in col_list]
                (p, s) = get_prefix_suffix_length(cleaned_column, True)
                cleaned_column = [" ".join(w.split()[p:] if s == 0 else w.split()[p:-s]) for w in cleaned_column]
                cleaned_columns.append(cleaned_column)

            # write cleaned data to cleaned file
            write_cleaned_columns_to_file(dataset_name, df.head(), cleaned_columns)
        else:
            shutil.copyfile(os.path.join(datasets_input_directory, dataset_name),
                            os.path.join(datasets_output_directory, dataset_name))


if __name__ == '__main__':
    main()

