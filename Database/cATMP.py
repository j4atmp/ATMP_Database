import streamlit as st
import os
from coversheet import coversheet_creator
from streamlit_gsheets import GSheetsConnection


CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # [ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # catmp.iloc[ATMP_ID][1] == ID_Value
catmps = []

conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

path = os.path.join(os.getcwd(), "all_dfs.pkl")

# Cover Sheet for cATMP
st.title('cATMP')
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]
# filter for cATMPs
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_CATEGORY][1] == 'cATMP':
        catmps.append(chunk)


if len(catmps) > 0 :
    # get the list of all cATMPs
    all_catmp_IDs = [str(catmp.iloc[ATMP_ID][1]) for catmp in catmps]
    all_catmp_IDs.sort()
    # select the cATMP and create selctbox
    option = st.selectbox(
        "cATMP List",
        options=all_catmp_IDs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected catmp
    for catmp in catmps:
        if option == str(catmp.iloc[ATMP_ID][1]):
            coversheet_creator(catmp, category='cATMP')
else:
    st.write('Nothing here yet!')