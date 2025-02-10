import streamlit as st
from utilities import coversheet_creator
from streamlit_gsheets import GSheetsConnection

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # chunk.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # tep.iloc[ATMP_ID][1] == ID_Value
teps = []

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# Cover Sheet for TEP
st.title('TEP')
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]
# filter for TEPs
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_CATEGORY][1] == 'TEP':
        teps.append(chunk)


if len(teps) > 0 :
    # get the list of all TEPs
    all_tep_IDs = [str(tep.iloc[ATMP_ID][1]) for tep in teps]
    all_tep_IDs.sort()
    # select the TEP and create selctbox
    option = st.selectbox(
        "TEP List",
        options=all_tep_IDs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected TEP
    for tep in teps:
        if option == str(tep.iloc[ATMP_ID][1]):
            coversheet_creator(tep)
else:
    st.write('Nothing here yet!')