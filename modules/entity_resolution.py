import pandas as pd
from rapidfuzz import fuzz

def calculate_similarity(a, b):
    return fuzz.token_sort_ratio(str(a), str(b)) / 100


def match_records(df1, df2):
    matches = []

    for _, row1 in df1.iterrows():
        for _, row2 in df2.iterrows():

            name_score = calculate_similarity(row1['name'], row2['name'])

            address_score = 0
            if 'address' in row1 and 'address' in row2:
                address_score = calculate_similarity(row1['address'], row2['address'])

            gst_score = 1 if ('gst' in row1 and pd.notna(row1.get('gst'))) else 0

            final_score = (0.5 * name_score) + (0.3 * address_score) + (0.2 * gst_score)

            matches.append({
                "name1": row1['name'],
                "name2": row2['name'],
                "score": round(final_score, 2),
                "reason": f"name:{round(name_score,2)}, address:{round(address_score,2)}, gst:{gst_score}"
            })

    return pd.DataFrame(matches)


def assign_ubid(matches_df):
    matches_df = matches_df.copy()
    matches_df["UBID"] = None

    ubid_counter = 1

    for i in range(len(matches_df)):
        if matches_df.loc[i, "score"] > 0.7:
            matches_df.loc[i, "UBID"] = f"UB{ubid_counter:03d}"
            ubid_counter += 1

    return matches_df