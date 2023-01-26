import os
import json
from pathlib import Path

import pandas as pd


def get_all_datasets(datasets_path):
    res = []

    for path in os.listdir(datasets_path):
        if os.path.isfile(os.path.join(datasets_path, path)):
            res.append(path)

    return res


def get_mappings():
    mappings_file = "config/schema_align/mappings.json"
    with open(mappings_file) as json_file:
        mappings = json.load(json_file)

    return mappings


def rename_columns(schema_name, mappings):
    datasets_path = 'datasets/cleaned/'
    schema = pd.read_csv(os.path.join(datasets_path, schema_name), encoding='ISO-8859-1')

    columns = []
    for col in schema.columns:
        if col in mappings:
            columns.append(mappings[col])
        else:
            schema = schema.drop(col, axis=1)

    schema.name = schema_name
    schema.columns = columns
    return schema


def main():
    schemas = []

    mappings = get_mappings()

    datasets_path = 'datasets/cleaned/'
    schemas_names = get_all_datasets(datasets_path)

    for schema_name in schemas_names:
        schemas.append(rename_columns(schema_name, mappings))

    big_schema = pd.DataFrame()

    for schema in schemas:
        print("Concat " + schema.name)
        big_schema = pd.concat([big_schema, schema], axis=0)

        filepath = Path('datasets/aligned_schema/schemas/' + schema.name)
        filepath.parent.mkdir(parents=True, exist_ok=True)
        schema.to_csv(filepath)

    filepath = Path('datasets/aligned_schema/aligned.csv')
    filepath.parent.mkdir(parents=True, exist_ok=True)
    big_schema.to_csv(filepath)


if __name__ == '__main__':
    main()
