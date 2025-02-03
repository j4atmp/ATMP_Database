import streamlit as st
import joblib
from coversheet import coversheet_creator
import os

path = os.path.join(os.getcwd(), "all_dfs.pkl")

# Cover Sheet for cATMP
st.title('cATMP')
# load the data
all_dfs = joblib.load(path)

if 'cATMP' in all_dfs.keys():
    # get the list of all cATMPs
    all_cATMPs = list(all_dfs['cATMP'].keys())
    all_cATMPs.sort()
    # select the cATMP and create selctbox
    option = st.selectbox(
        "cATMP List",
        options=all_cATMPs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected cATMP
    for i in all_cATMPs:
        if option == i:
            coversheet_creator(all_dfs, category='cATMP', atmp=i)
else:
    st.write('Nothing here yet!')
