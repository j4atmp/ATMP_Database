import streamlit as st
import os

path_logo = os.path.join(os.getcwd(),"Database/pages", "logo.png")

st.image(path_logo, width=400)

st.title('ATMP Database')
st.write(
"""
This web app is developed by the Medical University of Vienna as part of [J4ATMP Homepage](https://join4atmp.eu/) consortium. 
""")