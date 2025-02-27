import streamlit as st
import io
import pandas as pd
import warnings
from utilities import data_processing, check_password

warnings.filterwarnings('ignore')

ATMP_ID = 1 # atmp.iloc[ATMP_ID][1] == ID_Value
category_check = ['GTMP', 'TEP', 'sCTMP', 'cATMP']

def coversheet_creator(atmp, conn, all_dfs_chunks):

    st.title(atmp.iloc[ATMP_ID][1])

    # Donwload option as Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        data_processing(atmp.iloc[1:14]).to_excel(writer, sheet_name='ATMP Cover Sheet', index=False)
        data_processing(atmp.iloc[16:35]).to_excel(writer, sheet_name='Regulatory Information', index=False)
        data_processing(atmp.iloc[36:57]).to_excel(writer, sheet_name='WP 1', index=False)
        data_processing(atmp.iloc[58:,:2]).to_excel(writer, sheet_name='Review Status Information', index=False)
        writer.close()
        st.download_button(
                label = 'Download as Excel',
                data = buffer,
                file_name = f'{atmp.iloc[ATMP_ID][1]}.xlsx',
                mime='application/vnd.ms-excel'
        )

    # Cover Sheet Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1', 'Review Status Information', 'Edit ATMP'])

    with tab1:
        # Tab for ATMP Cover Sheet
        st.subheader('ATMP Cover Sheet')
        # Process rows 1 to 13 in the atmp dataframe
        cs = data_processing(atmp.iloc[1:14])
        # Display the dataframe
        st.dataframe(cs, hide_index=True, use_container_width=True, height=458)

    with tab2:
        # Tab for Regulatory Information
        st.subheader('Regulatory Information')
        # Process rows 16 to 34 in the atmp dataframe
        ri = data_processing(atmp.iloc[16:35])
        # Display the dataframe
        st.dataframe(ri, hide_index=True, use_container_width=True, height=668)

    with tab3:
        # Tab for WP 1
        st.subheader('WP 1')
        # Process rows 38 to 56 in the atmp dataframe
        wp1 = data_processing(atmp.iloc[36:57])
        # Display the dataframe
        st.dataframe(wp1, hide_index=True, use_container_width=True, height=773)

    with tab4:
        # Tab for Review Status Information
        st.subheader('Review Status Information')
        # Process rows 58 and 59 in the atmp dataframe
        rs = data_processing(atmp.iloc[58:,:2])
        # Display the dataframe
        st.dataframe(rs, hide_index=True)

    with tab5:
        # Check for WP1 User
        if not check_password():
            st.stop()

        # create tmp df for atmp to edit
        tmp_df = atmp.copy()
        tmp_all_dfs_chunks = all_dfs_chunks.copy()
        edited_df = atmp.copy()

        # Tab for ATMP Cover Sheet
        st.subheader('ATMP Cover Sheet')
        edited_df.iloc[1:15] = st.data_editor(tmp_df.iloc[1:15], hide_index=True, use_container_width=True, height=458, disabled=[tmp_df.iloc[1:15].columns[0]])
        # Tab for Regulatory Information
        st.subheader('Regulatory Information')
        edited_df.iloc[16:35] = st.data_editor(tmp_df.iloc[16:35], hide_index=True, use_container_width=True, height=458, disabled=[tmp_df.iloc[16:35].columns[0]])
        # Tab for WP 1
        st.subheader('WP 1')
        edited_df.iloc[36:57] = st.data_editor(tmp_df.iloc[36:57], hide_index=True, use_container_width=True, height=458, disabled=[tmp_df.iloc[36:57].columns[0]])
        # Tab for Review Status Information
        st.subheader('Review Status Information')
        edited_df.iloc[58:,:2] = st.data_editor(tmp_df.iloc[58:,:2], hide_index=True, use_container_width=True, height=458, disabled=[tmp_df.iloc[58:,:2].columns[0]])       
        # update tmp chunks atmps
        if st.button('Save changes and update ATMP'):
            if edited_df.iloc[14][1] in category_check:
                for index, chunk in enumerate(tmp_all_dfs_chunks):
                    
                    if chunk.iloc[ATMP_ID][1] == edited_df.iloc[ATMP_ID][1]:
                        tmp_all_dfs_chunks[index] = edited_df
                # update current atmp_df
                new_df = pd.concat(tmp_all_dfs_chunks, ignore_index=True)
                # update masterfile
                conn.update(data=new_df)
                st.write("Update successful!")
            else:
                st.write(f'**:red[Changes of ATMP do not contain a right ATMP category {category_check}]**')
            
