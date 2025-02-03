import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from checkpassword import check_password
from coversheet import coversheet_creator


path_dataframes = os.path.join(os.getcwd(), "all_dfs.pkl")
path_coversheets = os.path.join(os.getcwd(), "ATMP Sheets")

st.title('Upload ATMP-Sheet')
# load the data
all_dfs = joblib.load(path_dataframes)
all_gtmps = list(all_dfs['GTMP'].keys())
all_gtmps.sort()

if not check_password():
    st.stop()


category = st.selectbox(
    "Choose ATMP category",
    options=['GTMP', 'TEP'],
    index=None,
    placeholder="GTMP"
)
if category is not None:
    uploaded_files = st.file_uploader(
        "Choose an ATMP in the right Format (see Cover Sheet Example)", 
        accept_multiple_files=True,
        type = 'xlsx'
    )

    for uploaded_file in uploaded_files:
        tmp = pd.read_excel(uploaded_file, skiprows=(0, 14, 35), header=None, index_col=0)
        tmp = tmp.T
        tmp = tmp.drop(columns=np.nan)
        atmp_id = tmp[tmp.columns[0]].iloc[0]
       
        all_dfs[category][atmp_id] = tmp

        joblib.dump(all_dfs, 'all_dfs.pkl')



          
          