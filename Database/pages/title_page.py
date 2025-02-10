import streamlit as st
import os

path_logo = os.path.join(os.getcwd(),"Database/pages", "logo.png")

st.title('ATMP-Database')

st.image(path_logo, width=800)

st.link_button("J4ATMP Homepage", 'https://join4atmp.eu/')