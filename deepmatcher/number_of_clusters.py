from pathlib import Path

import pandas as pd
import networkx as nx


def number_of_clusters(thresh):
    min_prob_thresh = thresh

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

    return nx.number_connected_components(G)


def main():
    for i in range(10, 100, 8):
        conn_comp = number_of_clusters(i / 100)
        print(str(i) + "," + str(conn_comp))


if __name__ == '__main__':
    main()
