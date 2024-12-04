import streamlit as st
import joblib

st.title('Download')

option = st.selectbox(
    "Formats",
    options=('CSV', 'EXCEL', 'PKL'),
    index=None,
    placeholder="Choose an Option"
)

if option == 'PKL':
    st.download_button(
        label="Download data as PKL",
        data='/..all_dfs.pkl',
        file_name="ATMPS.pkl",
    )
elif option == 'CSV' or option == 'EXCEL':
    st.write('Not implemented yet!')