import streamlit as st
from utilities import coversheet_creator
from streamlit_gsheets import GSheetsConnection

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # chunk.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # sctmp.iloc[ATMP_ID][1] == ID_Value
sctmps = []

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# Cover Sheet for sCTMP
st.title('sCTMP')
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]
# filter for sCTMPs
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_CATEGORY][1] == 'sCTMP':
        sctmps.append(chunk)


if len(sctmps) > 0 :
    # get the list of all sCTMPs
    all_sctmp_IDs = [str(sctmp.iloc[ATMP_ID][1]) for sctmp in sctmps]
    all_sctmp_IDs.sort()
    # select the sCTMP and create selctbox
    option = st.selectbox(
        "sCTMP List",
        options=all_sctmp_IDs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected sCTMP
    for sctmp in sctmps:
        if option == str(sctmp.iloc[ATMP_ID][1]):
            coversheet_creator(sctmp)
else:
    st.write('Nothing here yet!')