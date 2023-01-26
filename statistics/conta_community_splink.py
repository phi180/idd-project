from pathlib import Path

import pandas as pd
import networkx as nx


def number_of_clusters(thresh):
    min_prob_thresh = thresh

    matchings_dataset = pd.read_csv('../datasets/4_record_linkage/splink/matchings.csv')

    filtered_df = matchings_dataset.loc[matchings_dataset['match_probability'] > min_prob_thresh]

    G = nx.Graph()

    # need to get all nodes
    left = list(filtered_df['unique_id_l'])
    right = list(filtered_df['unique_id_r'])

    nodes = list(set(left + right))

    G.add_nodes_from(nodes)

    edges = filtered_df[['unique_id_l', 'unique_id_r']].apply(tuple, axis=1)
    G.add_edges_from(edges)

    return nx.number_connected_components(G)


def main():
    for i in range(10, 100, 8):
        conn_comp = number_of_clusters(i / 100)
        print(str(i) + "," + str(conn_comp))


if __name__ == '__main__':
    main()
