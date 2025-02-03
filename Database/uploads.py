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

st.markdown('''
    For uploading ATMP-Sheets you need a User login.   
    If you have no User Login there are two options:
            
        1. send Email with the ATMP 
        2. or send Email to register for a user*
    to j4atmp@gmail.com.
    
    **:red[Please always use the Template Format and do not change it!!!]**
    
    *here you need to state your affiliation to J4ATMP and Personal Information.
    ''')


st.subheader('Cover Sheet Example (as Template)')

file = 'Database/ATM_Cover_Sheet_Example.xlsx'

with open(file, 'rb') as my_file:
    st.download_button(label = ':arrow_down: Download Template Excel file', 
    data = my_file, 
    file_name = 'ATMP_Cover_Sheet_Example.xlsx', 
    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      


if not check_password():
    st.stop()


category = st.selectbox(
    "Choose ATMP category",
    options=['GTMP', 'TEP', 'sCTMP','cATMP'],
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
        data_upload = pd.read_excel(uploaded_file, skiprows=(0, 14, 35), header=None, index_col=0)
        data_upload = data_upload.T
        data_upload = data_upload.drop(columns=np.nan)
        adata_upload_id = data_upload[data_upload.columns[0]].iloc[0]
        if category in all_dfs.keys():
            continue
        else:
            all_dfs[category] = dict()
        all_dfs[category][adata_upload_id] = data_upload

        joblib.dump(all_dfs, 'all_dfs.pkl')
        


          
          