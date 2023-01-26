from pathlib import Path

from splink.duckdb.duckdb_linker import DuckDBLinker
from splink.duckdb.duckdb_comparison_library import (
    exact_match,
    levenshtein_at_thresholds,
)

import pandas as pd


dataset_input_path = 'datasets/aligned_schema/out_manual.csv'
dataset_output_linkage = 'datasets/rl/splink/linkage.csv'
dataset_output_clusters = 'datasets/rl/splink/clusters.csv'

def main():
    df = pd.read_csv(dataset_input_path)

    settings = {
        "link_type": "dedupe_only",
        "blocking_rules_to_generate_predictions": [
            "l.company_name = r.company_name",
        ],
        "comparisons": [
            levenshtein_at_thresholds("company_name", 3),
            levenshtein_at_thresholds("company_industry", 20),
            levenshtein_at_thresholds("company_location", 20)
        ],
    }

    linker = DuckDBLinker(df, settings)
    linker.estimate_u_using_random_sampling(target_rows=1e6)

    blocking_rule_for_training = "l.company_name = r.company_name"
    linker.estimate_parameters_using_expectation_maximisation(blocking_rule_for_training)

    pairwise_predictions = linker.predict()

    filepath = Path(dataset_output_linkage)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    pairwise_predictions.as_pandas_dataframe().to_csv(filepath)

    clusters = linker.cluster_pairwise_predictions_at_threshold(pairwise_predictions, 0.55)

    filepath = Path(dataset_output_clusters)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    clusters.as_pandas_dataframe().to_csv(filepath)


if __name__ == '__main__':
    main()

