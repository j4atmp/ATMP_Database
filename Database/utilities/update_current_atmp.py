import streamlit as st
import pandas as pd

ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

def update_atmp(uploaded_files, Current_Atmps, all_dfs, all_dfs_chunks, template, conn):
    tmp_dfs_update_ATMPS = []
    tmp_all_dfs_chunks = all_dfs_chunks.copy()
    tmp_all_dfs = all_dfs.copy()
    category_check = ['GTMP', 'TEP', 'sCTMP', 'cATMP']

    for uploaded_file in uploaded_files:
        data_upload = pd.read_excel(uploaded_file, header=None)
        # check if there are less than two columns => no new content as column 1 are the fields
        if len(data_upload.columns) < 2:
            st.markdown(f'ATMP **:red[{uploaded_file.name}]** doesn`t contain content!')
        # check if all fileds are the same and in the same order as in the template
        elif [s.rstrip() for s in list(data_upload[0])] == [s.rstrip() for s in list(template['FIELDS'])]:
            if data_upload.iloc[14][1] in category_check:
                st.markdown(f'**:green[{uploaded_file.name}]** no Errors found!')
                # check if the ATMPs are already in the master file
                if data_upload.iloc[ATMP_ID][1] in Current_Atmps:
                    # load uploaded files into tmp list
                    tmp_dfs_update_ATMPS.append(data_upload)
                else:
                    st.markdown(f'ATMP **:red[{uploaded_file.name}]** does not exist! Please use Upload!')
            else:
                st.write(f'**:red[{uploaded_file.name}]** does not contain a right ATMP category {category_check}') 
        else:
            st.markdown(f'File format for **:red[{uploaded_file.name}]** is **not correct**! Please check with Cover Sheet Example!') 

    # Update current ATMPs
    if len(tmp_dfs_update_ATMPS) > 0:
        update_button = st.button(label = 'Update all correct ATMPs')  
        if update_button:
            for new_atmp_file in tmp_dfs_update_ATMPS:
                # change columns to match master sheet format
                if len(new_atmp_file.columns) > len(tmp_all_dfs.columns):
                    for i in range(len(tmp_all_dfs.columns) - 1 , len(new_atmp_file.columns) - 1):
                        tmp_all_dfs[f'Unnamed: {i+1}'] = None  # Adds empty (NaN) columns
                else:
                    for i in range(len(new_atmp_file.columns) - 1 , len(tmp_all_dfs.columns) - 1):
                        new_atmp_file[f'Unnamed: {i+1}'] = None  # Adds empty (NaN) columns
                new_atmp_file.columns = tmp_all_dfs.columns
                # update tmp chunks atmps
                for index, chunk in enumerate(tmp_all_dfs_chunks):
                    if chunk.iloc[ATMP_ID][1] == new_atmp_file.iloc[ATMP_ID][1]:
                        tmp_all_dfs_chunks[index] = new_atmp_file
                # search max columns
                max_columns = max(len(df.columns) for df in tmp_all_dfs_chunks)
                # change columns to match each other
                for chunk in tmp_all_dfs_chunks:
                    if max_columns > len(chunk.columns):
                        for i in range(max_columns - len(chunk.columns)):
                            chunk[f'New_Col_{i+1}'] = None  # Adds empty (NaN) columns
            # update current atmp_df
            new_df = pd.concat(tmp_all_dfs_chunks, ignore_index=True)
            # update masterfile
            conn.update(data=new_df)
            st.write("Update successful!")