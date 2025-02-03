import streamlit as st
import joblib
from coversheet import coversheet_creator
import os

path = os.path.join(os.getcwd(), "all_dfs.pkl")

# Cover Sheet for TEP
st.title('TEP')
# load the data
all_dfs = joblib.load(path)

if 'cATMP' in all_dfs.keys():
    # get the list of all TEPs
    all_teps= list(all_dfs['TEP'].keys())
    all_teps.sort()
    # select the TEP and create selctbox
    option = st.selectbox(
        "TEP List",
        options=all_teps,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected TEP
    for i in all_teps:
        if option == i:
            coversheet_creator(all_dfs, category='TEP', atmp=i)
else:
    st.write('Nothing here yet!')
