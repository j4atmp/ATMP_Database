import streamlit as st
import joblib

all_dfs = joblib.load('../all_dfs.pkl')

cat_first = list(all_dfs.keys())[0]
atmp_first = list(all_dfs[cat_first].keys())[0]
all_fields = list(all_dfs[cat_first][atmp_first].columns)

st.title('Search')

option = st.selectbox(
    "Search List",
    options=all_fields,
    index=None,
    placeholder="Choose a Field to search"
)

if option:
    search_term = st.text_input(label='insert search term')

st.write('Not implemented yet!')