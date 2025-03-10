import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import warnings
warnings.filterwarnings("ignore")

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

options_cs = list(all_dfs_chunks[0]['FIELDS'][1:14])
options_ri = list(all_dfs_chunks[0]['FIELDS'][16:35])
options_wp1 = list(all_dfs_chunks[0]['FIELDS'][36:57])
options_rsi = list(all_dfs_chunks[0]['FIELDS'][58:])

options = options_cs + options_ri + options_wp1 + options_rsi
options.sort()

st.title('Search')


option = st.selectbox(
    "Search List",
    options=options,
    index=None,
    placeholder="Choose a Field to search"
)

if option:
    tmp = []
    for chunk in all_dfs_chunks:
        for col in chunk[chunk['FIELDS']==option].columns:
            if col == 'FIELDS':
                continue
            for unique_value in chunk[chunk['FIELDS']==option][col]:
                if pd.notna(unique_value):
                    if option == 'Study title' or option == 'Animal studies':
                        if unique_value not in tmp:
                            tmp.append(unique_value)
                    else:
                        for i in unique_value.split(', '):
                            if i.rstrip() not in tmp:
                                tmp.append(i.rstrip())
    if len(tmp) == 0:
        st.write('No Entries in this Category found!')
    else:
        option2 = st.selectbox(
        "Availabel Options",
        options=tmp,
        index=None,
        placeholder="Choose a Field to search")

        if option2:
            found_atmps = {'ATMPs': [], 'ATMP Category':[]}
            for chunk in all_dfs_chunks:
                tmp_2 = [i for i in chunk[chunk['FIELDS']==option].iloc[0][1:] if pd.notna(i)]
                if len(tmp_2) == 0:
                    continue
                if option2 in '; '.join(tmp_2):
                    found_atmps['ATMPs'].append(chunk.iloc[1][1])
                    found_atmps['ATMP Category'].append(chunk.iloc[ATMP_CATEGORY][1])
            st.subheader(f'Found {len(found_atmps["ATMPs"])} ATMPs with specified values')
            st.dataframe(found_atmps)
