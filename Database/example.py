import streamlit as st
import joblib
from coversheet import coversheet_creator

st.title('Cover Sheet Example (as Template)')

file = 'Database/ATM_Cover_Sheet_Example.xlsx'

with open(file, 'rb') as my_file:
    st.download_button(label = ':arrow_down: Download Template Excel file', 
    data = my_file, 
    file_name = 'ATMP_Cover_Sheet_Example.xlsx', 
    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      
