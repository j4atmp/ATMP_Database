import streamlit as st
from utilities import coversheet_creator
from streamlit_gsheets import GSheetsConnection

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # chunk.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # gtmp.iloc[ATMP_ID][1] == ID_Value
gtmps = []

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# Cover Sheet for GTMP
st.title('GTMP')
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]
# filter for GTMPs
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_CATEGORY][1] == 'GTMP':
        gtmps.append(chunk)


if len(gtmps) > 0 :
    # get the list of all GTMPs
    all_gtmp_IDs = [str(gtmp.iloc[ATMP_ID][1]) for gtmp in gtmps]
    all_gtmp_IDs.sort()
    # select the GTMP and create selctbox
    option = st.selectbox(
        "GTMP List",
        options=all_gtmp_IDs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected GTMP
    for gtmp in gtmps:
        if option == str(gtmp.iloc[ATMP_ID][1]):
            coversheet_creator(gtmp)
else:
    st.write('Nothing here yet!')