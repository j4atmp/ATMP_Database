import streamlit as st
import joblib
import os
import pandas as pd
import numpy as np
from streamlit_gsheets import GSheetsConnection
from utilities import check_password

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

st.title('Upload ATMP-Sheet')
# load the data

st.markdown('''
    For uploading ATMP-Sheets you need the WP1 User.   
    If you don't have a WP1 User for login there are two options:
            
        1. send an Email with the ATMP* 
        2. or send an Email to register for the WP1 User*
    to j4atmp@gmail.com.

    *In both cases you need to state your affiliation to J4ATMP and Personal Information.
    
    **:red[Please always use the Template Format and do not change it!!!]**
    
    ''')


st.subheader('Cover Sheet Example (as Template)')

file = 'Database/pages/ATM_Cover_Sheet_Example.xlsx'

with open(file, 'rb') as my_file:
    st.download_button(label = ':arrow_down: Download Template Excel file', 
    data = my_file, 
    file_name = 'ATMP_Cover_Sheet_Example.xlsx', 
    mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')      

template = pd.read_excel(file, header=None)

# create list of current ATMP IDs
Current_Atmps = set()
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_ID][1] not in Current_Atmps:
        Current_Atmps.add(chunk.iloc[ATMP_ID][1])

# Check for WP1 User
if not check_password():
    st.stop()


uploaded_files = st.file_uploader(
    "Choose an ATMP in the right Format (see Cover Sheet Example)", 
    accept_multiple_files=True,
    type = 'xlsx'
)

new_df = all_dfs.copy()
tmp_dfs_new_ATMPS = []
tmp_dfs_update_ATMPS = []



for uploaded_file in uploaded_files:
    data_upload = pd.read_excel(uploaded_file, header=None)
    
    # check if there are less than two columns => no new content as column 1 are the fields
    if len(data_upload.columns) < 2:
        st.markdown(f'ATMP **:red[{uploaded_file.name}]** doesn`t contain content!')
    # check if all fileds are the same and in the same order as in the template
    elif [s.rstrip() for s in list(data_upload[0])] == [s.rstrip() for s in list(template[0])]:
        st.markdown(f'**:green[{uploaded_file.name}]** no Errors found!')
        # check if the ATMPs are already in the master file
        if data_upload.iloc[ATMP_ID][1] not in Current_Atmps:
            # load uploaded files into tmp list
            tmp_dfs_new_ATMPS.append(data_upload)
        # update ATMP
        else:
            st.markdown(f'ATMP **:red[{uploaded_file.name}]** already exists!')
            # load uploaded files into tmp list for updates
            tmp_dfs_update_ATMPS.append(data_upload)
    else:
        st.markdown(f'File format for **:red[{uploaded_file.name}]** is **not correct**! Please check with Cover Sheet Example!') 

# Update ATMPs         
if len(tmp_dfs_update_ATMPS) > 0:
        pass

# Upload new ATMPs
if len(tmp_dfs_new_ATMPS) > 0:
    upload_button = st.button('Upload all correct new ATMPs!')  
    if upload_button:
        for new_atmp_file in tmp_dfs_new_ATMPS:
            # change colums to match each other
            if len(new_atmp_file.columns) > len(all_dfs.columns):
                for i in range(len(new_atmp_file.columns) - len(all_dfs.columns)):
                    all_dfs[f'New_Col_{i+1}'] = None  # Adds empty (NaN) columns
            else:
                for i in range(len(all_dfs.columns) - len(new_atmp_file.columns)):
                    new_atmp_file[f'Unnamed: {i+1}'] = None  # Adds empty (NaN) columns
            new_atmp_file.columns = all_dfs.columns
            # append new_atmp_df to current atmp_df
            new_df = pd.concat([new_df, new_atmp_file], ignore_index=True)
        # update masterfile
        conn.update(data=new_df)
        st.write("Upload successful!")