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
            for unique_value in chunk[chunk['FIELDS']==option][col].unique():
                if pd.notna(unique_value):
                    for i in unique_value.split(', '):
                        if i.rstrip() not in tmp:
                            tmp.append(i.rstrip())


    option2 = st.selectbox(
    "Availabel Options",
    options=tmp,
    index=None,
    placeholder="Choose a Field to search")

    
   

    if option2:
        found_atmps = []
        for chunk in all_dfs_chunks:
            tmp_2 = [i for i in chunk[chunk['FIELDS']==option].iloc[0][1:] if pd.notna(i)]
            if option2 in tmp_2[0]:
                found_atmps.append((chunk.iloc[1][1], chunk.iloc[ATMP_CATEGORY][1]))
        st.subheader(f'Found {len(found_atmps)} ATMPs with specified values')
        for value in found_atmps:
            st.write(value[0], '| ATMP Category:', value[1])
