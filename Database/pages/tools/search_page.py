import streamlit as st
import pandas as pd
from utilities import coversheet_creator
from streamlit_gsheets import GSheetsConnection
import warnings
warnings.filterwarnings("ignore")

CHUNK_SIZE = 59
ATMP_CATEGORY = 13 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

options_cs = list(all_dfs_chunks[0]['FIELDS'][1:13])
options_ri = list(all_dfs_chunks[0]['FIELDS'][15:34])
options_wp1 = list(all_dfs_chunks[0]['FIELDS'][35:56])
options_rsi = list(all_dfs_chunks[0]['FIELDS'][57:2])

options_raw = options_cs + options_ri + options_wp1 + options_rsi
options = []
for i in options_raw:
    if i not in options:
        options.append(i)
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
            found_atmps = []
            for chunk in all_dfs_chunks:
                tmp_2 = [i for i in chunk[chunk['FIELDS']==option].iloc[0][1:] if pd.notna(i)]
                if len(tmp_2) == 0:
                    continue
                if option2 in '; '.join(tmp_2):
                    found_atmps.append(chunk.iloc[1][1] + ' | '+ chunk.iloc[ATMP_CATEGORY][1])
            st.subheader(f'Found {len(found_atmps)} ATMPs with specified values')
            selection = st.segmented_control(
                'To see data select ATMP', found_atmps)
            if selection:
                for chunk in all_dfs_chunks:
                    if chunk.iloc[1][1] in selection:
                        coversheet_creator(chunk, conn, all_dfs_chunks)
               
