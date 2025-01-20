import streamlit as st
import os

path_logo = os.path.join(os.getcwd(),"Database", "logo.png")

st.title('ATMP-Database')

st.image(path_logo, width=300)
