from pathlib import Path

import time

from splink.duckdb.duckdb_linker import DuckDBLinker
from splink.duckdb.duckdb_comparison_library import (
    exact_match,
    levenshtein_at_thresholds,
)

import time

import pandas as pd
import numpy as np


dataset_input_path = 'datasets/3_aligned_schema/aligned.csv'
dataset_output_linkage = 'datasets/4_record_linkage/splink/linkage_result.csv'
dataset_output_clusters = 'datasets/4_record_linkage/splink/clusters.csv'
dataset_output_final = 'datasets/4_record_linkage/splink/result.csv'


def main(leven_dist):
    start = time.time()
    df = pd.read_csv(dataset_input_path)

    # assigns unique id to each record
    df = df.reset_index()
    df = df.rename(columns={"index": "unique_id"})
    df['unique_id'] = df.index

    blocking_rule = "substr(lower(l.company_name), 1, 6) = substr(lower(r.company_name), 1, 6)"

    settings = {
        "link_type": "dedupe_only",
        "blocking_rules_to_generate_predictions": [
            blocking_rule
        ],
        "comparisons": [
            levenshtein_at_thresholds("company_name", leven_dist),
            levenshtein_at_thresholds("company_industry", 20)
            # levenshtein_at_thresholds("company_location", 20)
        ],
    }

    linker = DuckDBLinker(df, settings)
    linker.estimate_u_using_random_sampling(target_rows=1e6)

    blocking_rule_for_training = "l.company_name = r.company_name"
    linker.estimate_parameters_using_expectation_maximisation(blocking_rule_for_training)

    pairwise_predictions = linker.predict()

    filepath = Path("datasets/4_record_linkage/splink/" + str(int(time.time())) + str(leven_dist) + ".csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    pairwise_predictions.as_pandas_dataframe().to_csv(filepath)

    clusters = linker.cluster_pairwise_predictions_at_threshold(pairwise_predictions, 0.55)

    end = time.time()
    print("Elapsed time in: " + str(end - start) + " for leven=" + str(i))

    filepath = Path(dataset_output_clusters)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    clusters_dataframe = clusters.as_pandas_dataframe()

    clusters_dataframe.to_csv(filepath)

    clusters_dataframe = clusters_dataframe.astype(str)
    final_dataset = clusters_dataframe.groupby('cluster_id').agg(
        {
            'company_name': np.max,
            'company_industry': np.max,
            'company_location': np.max,
            'company_founded': np.max,
            'company_country': np.max,
            'company_ceo': np.max,
            'company_employees': np.max,
            'company_revenue': np.max
        }
    )

    filepath = Path(dataset_output_final)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    final_dataset.to_csv(filepath)

if __name__ == '__main__':
    for i in [2,5,7,9,11]:
        print("Leven dist = " + str(i))
        start = time.time()
        main(i)
        end = time.time()
        print("Elapsed time out: " + str(end - start) + " for leven=" + str(i))


