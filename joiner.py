from pathlib import Path

import pandas as pd

matchings = pd.read_csv("deepmatcher/dataset/unlabeled.csv")
matchings = matchings.rename(columns={"company_name": "right_company_name",
                                      "company_industry": "right_company_industry",
                                      "company_location": "right_company_location",
                                      "company_founded": "right_company_founded",
                                        "company_rank": "right_company_rank",
                                        "company_country": "right_company_country",
                                        "company_revenue": "right_company_revenue",
                                        "company_ipo_code": "right_company_ipo_code",
                                        "company_facebook": "right_company_facebook",
                                        "company_twitter": "right_company_twitter",
                                        "company_instagram": "right_company_instagram",
                                        "company_employees": "right_company_employees",
                                        "company_ceo": "right_company_ceo",
                                        "company_top_competitor": "right_company_top_competitor",
                                        "company_founder": "right_company_founder",
                                        "company_ipo_year": "right_company_ipo_year"
                                      })
filepath = Path('deepmatcher/dataset/unlabeled.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
matchings.to_csv(filepath)

'''
aligned_df = pd.read_csv("datasets/3_aligned_schema/aligned_with_id.csv")

big_schema = pd.merge(matchings, aligned_df, left_on='unique_id_r', right_on='unique_id',
         how='left', suffixes=('_1', '_1'))
#big_schema.columns = big_schema.columns.str.replace('company', 'right_company')

big_schema = pd.merge(big_schema, aligned_df, left_on='unique_id_r', right_on='unique_id',
         how='left', suffixes=('_1', '_1'))
filepath = Path('deepmatcher/dataset/unlabeled.csv')
filepath.parent.mkdir(parents=True, exist_ok=True)
big_schema.to_csv(filepath)'''

