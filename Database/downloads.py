import streamlit as st

st.title('Download')

option = st.selectbox(
    "Formats",
    options=('CSV', 'EXCEL', "PKL"),
    index=None,
    placeholder="Choose an Option"
)