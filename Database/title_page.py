import streamlit as st
import joblib

all_dfs = joblib.load('../all_dfs.pkl')

st.title('ATMP-Database')
