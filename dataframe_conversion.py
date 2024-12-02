import pandas as pd
import os

def df_converter():
    all_dfs = dict()

    os.chdir("ATMP Sheets")

    categories = os.listdir(os.curdir)

    for category in categories:
        if category in all_dfs.keys():
            continue
        else:
            all_dfs[category] = dict()
        for file in os.listdir(category):
            tmp = pd.read_excel(f'{category}/{file}', skiprows=(0, 14, 35), header=None, index_col=0)
            tmp = tmp.T
            atmp_id = tmp['Title of ATMP / ATMP identifyer / Investigational medicinal product name'].iloc[0]
            if atmp_id in all_dfs[category].keys():
                continue
            else:
                all_dfs[category][atmp_id] = tmp

    return all_dfs

if __name__ == "__main__":
    df_converter()

