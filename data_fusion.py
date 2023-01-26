from pathlib import Path

import pandas as pd

cluster_df = pd.read_csv("datasets/4_record_linkage/splink/clusters.csv")

max_cluster_id = cluster_df['cluster_id'].max() + 1

full_aligned_schema_df = pd.read_csv("datasets/3_aligned_schema/aligned_with_id_cluster.csv")
full_aligned_schema_df.insert(0, 'cluster_id', range(max_cluster_id, max_cluster_id + len(full_aligned_schema_df)))

ids_to_drop = list(cluster_df['unique_id'])

# elimina i duplicati
full_aligned_schema_df = full_aligned_schema_df[~full_aligned_schema_df['unique_id'].isin(ids_to_drop)]
full_aligned_schema_df = pd.concat([full_aligned_schema_df, cluster_df], ignore_index=True)

filepath = Path("full_with_clusters.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
full_aligned_schema_df.to_csv(filepath)

full_aligned_schema_df = full_aligned_schema_df.groupby('cluster_id', as_index=False).first()

filepath = Path("mediated.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
full_aligned_schema_df.to_csv(filepath)
