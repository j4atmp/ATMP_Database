import streamlit as st
import joblib
from coversheet import coversheet_creator

st.title('TEP')

all_dfs = joblib.load('../all_dfs.pkl')

all_teps= list(all_dfs['TEP'].keys())
all_teps.sort()

option = st.selectbox(
    "TEP List",
    options=all_teps,
    index=None,
    placeholder="Choose an ATMP"
)

for i in all_teps:
    if option == i:
        coversheet_creator(all_dfs, category='TEP', atmp=i)
