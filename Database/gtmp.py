import streamlit as st
import joblib
from coversheet import coversheet_creator

all_dfs = joblib.load('../all_dfs.pkl')

all_gtmps = list(all_dfs['GTMP'].keys())
all_gtmps.sort()

for i in all_gtmps:
    if st.button(i):
        coversheet_creator(all_dfs, category='GTMP', atmp=i)