import streamlit as st
import joblib
from coversheet import coversheet_creator
import os
# Get the current working directory

path = os.path.join(os.getcwd(), "all_dfs.pkl")

# Cover Sheet for GTMP
st.title('GTMP')
st.subheader(path)
# load the data
all_dfs = joblib.load(path)
# get the list of all GTMPs
all_gtmps = list(all_dfs['GTMP'].keys())
all_gtmps.sort()
# select the GTMP and create selctbox
option = st.selectbox(
    "GTMP List",
    options=all_gtmps,
    index=None,
    placeholder="Choose an ATMP"
)
# create the coversheet for the selected GTMP
for i in all_gtmps:
    if option == i:
        coversheet_creator(all_dfs, category='GTMP', atmp=i)