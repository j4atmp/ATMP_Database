import streamlit as st
import joblib
from coversheet import coversheet_creator
import os

path = os.path.join(os.getcwd(), "all_dfs.pkl")

# Cover Sheet for sCTMP
st.title('sCTMP')
# load the data
all_dfs = joblib.load(path)

if 'sCTMP' in all_dfs.keys():
    # get the list of all sCTMPs
    all_sCTMPs = list(all_dfs['sCTMP'].keys())
    all_sCTMPs.sort()
    # select the sCTMP and create selctbox
    option = st.selectbox(
        "sCTMP List",
        options=all_sCTMPs,
        index=None,
        placeholder="Choose an ATMP"
    )
    # create the coversheet for the selected sCTMP
    for i in all_sCTMPs:
        if option == i:
            coversheet_creator(all_dfs, category='sCTMP', atmp=i)
else:
    st.write('Nothing here yet!')
