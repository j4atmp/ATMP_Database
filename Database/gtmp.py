import streamlit as st
import joblib
from coversheet import coversheet_creator

st.title('GTMP')

all_dfs = joblib.load('../all_dfs.pkl')

all_gtmps = list(all_dfs['GTMP'].keys())
all_gtmps.sort()

option = st.selectbox(
    "GTMP List",
    options=all_gtmps,
    index=None,
    placeholder="Choose an ATMP"
)

for i in all_gtmps:
    if option == i:
        coversheet_creator(all_dfs, category='GTMP', atmp=i)