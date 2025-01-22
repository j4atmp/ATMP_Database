import streamlit as st
import os

path_logo = os.path.join(os.getcwd(),"Database", "logo.png")

st.title('ATMP-Database')

st.image(path_logo, width=800)

st.link_button("J4ATMP Homepage", 'https://join4atmp.eu/')

st.write("""The JOIN4ATMP project aims to accelerate and 
         de-risk European ATMP development and 
         ensure wide-spread access of ATMPs, 
         through the mapping of obstacles to such development, 
         the audit of real-world-based solutions 
         and the definition of new paths forward.""")