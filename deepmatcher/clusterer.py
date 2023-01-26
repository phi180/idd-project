from pathlib import Path

import pandas as pd
import networkx as nx

min_prob_thresh = 0.7

matchings_dataset = pd.read_csv('dataset/.intermediary/matching_rich.csv')

filtered_df = matchings_dataset.loc[matchings_dataset['match_score'] > min_prob_thresh]

G = nx.Graph()

# need to get all nodes
left = list(filtered_df['left_unique_id'])
right = list(filtered_df['right_unique_id'])

nodes = list(set(left + right))

G.add_nodes_from(nodes)

edges = filtered_df[['left_unique_id', 'right_unique_id']].apply(tuple, axis=1)
G.add_edges_from(edges)

print(G)

aligned = pd.read_csv('dataset/.intermediary/aligned_with_id.csv')
aligned.set_index(keys='unique_id')

for id_cluster, ids in enumerate(nx.connected_components(G)):
    for id in ids:
        aligned.loc[aligned['unique_id'] == id, 'community'] = id_cluster

print(nx.number_connected_components(G))

'''
filepath = Path("dataset/aligned_cluster.csv")
filepath.parent.mkdir(parents=True, exist_ok=True)
aligned.to_csv(filepath)
'''