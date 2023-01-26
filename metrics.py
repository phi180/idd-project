import csv

import pandas as pd

datasets_dir = "datasets/4_record_linkage/splink/"
golden_path = "datasets/4_record_linkage/golden/golden.csv"
filenames = ["16757180552.csv", "16757182105.csv", "16757183357.csv", "16757185109.csv", "167571869411.csv"]

golden = pd.read_csv(golden_path)

results = []

for filename in filenames:
    dataset = pd.read_csv(datasets_dir + filename)
    df = pd.merge(golden, dataset, how='left',
                  left_on=['unique_id_l', 'unique_id_r'],
                  right_on=['unique_id_l', 'unique_id_r'])

    pd.set_option('display.max_columns', None)
    print(df.head(5))

    for prob_thresh in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9]:
        tp = len(df[(df['matches'] == True) & (df['match_probability'] >= prob_thresh)])
        fp = len(df[(df['matches'] == False) & (df['match_probability'] >= prob_thresh)])
        fn = len(df[(df['matches'] == True) & (df['match_probability'] < prob_thresh)])

        precision = tp / (tp + fp)
        recall = tp / (tp + fn)
        f1 = 2*(precision*recall)/(precision+recall)

        print("Dataset = " + filename)
        print("Prob thresh = " + str(prob_thresh))
        print("Precision = tp/(tp+fp) = " + str(precision))
        print("Recall = tp/(tp+fn) = " + str(recall))

        results.append((filename, prob_thresh, precision, recall, f1))


with open('results.csv', 'w', newline='') as out:
    csv_out = csv.writer(out)
    csv_out.writerow(['filename', 'prob_thresh', 'precision', 'recall', 'f1'])
    for row in results:
        csv_out.writerow(row)

print("==== END ====")
