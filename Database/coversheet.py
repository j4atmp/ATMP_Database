import streamlit as st
import numpy as np
import os
import io
import pandas as pd
import warnings
warnings.filterwarnings('ignore')


def coversheet_creator(all_dfs, category, atmp):
# ATMP Cover Sheet
    # columns 0-11
# Regulatory Information
    # columns 12-30
# WP 1
    # columns 31-51

    # selected ATMP
    st.title(atmp)

    # Donwload option as Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        all_dfs[category][atmp].iloc[:,0:13].T.to_excel(writer, sheet_name='ATMP Cover Sheet')
        all_dfs[category][atmp].iloc[:,14:33].T.to_excel(writer, sheet_name='Regulatory Information')
        all_dfs[category][atmp].iloc[:,34:55].T.to_excel(writer, sheet_name='WP 1')
        all_dfs[category][atmp].iloc[:,56].T.to_excel(writer, sheet_name='Status Information')
        writer.close()
        btn_single = st.download_button(
                label = 'Download as Excel',
                data = buffer,
                file_name = f'{atmp}.xlsx',
                mime='application/vnd.ms-excel'
        )

    # Cover Sheet Tabs
    tab1, tab2, tab3, tab4 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1', 'Status'])

    with tab1:
        # Tab for ATMP Cover Sheet
        st.subheader('ATMP Cover Sheet')
        # Process rows 2 to 14 in the Exel Sheet and transpose 
        cs = all_dfs[category][atmp].iloc[:,0:13].T
        # Set the index to the first row
        cs = cs.reset_index()
        # Rename the columns from 0 onwards
        cs.rename(columns={index : str(value) for index,value in enumerate(range(len(cs.columns))) }, inplace=True)
        # Rename the first column to 'Fields'
        cs.rename(columns={'0': 'Fields', 1: 'Values'}, inplace=True)
        # Drop columns with all NaN values
        cs = cs.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        cs.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(cs, hide_index=True, use_container_width=True, height=458)

    with tab2:
        # Tab for Regulatory Information
        st.subheader('Regulatory Information')
        # Process rows 17 to 35 in the Exel Sheet and transpose 
        ri = all_dfs[category][atmp].iloc[:,14:33].T
        # Set the index to the first row
        ri = ri.reset_index()
        # Rename the columns from 0 onwards
        ri.rename(columns={index : str(value) for index,value in enumerate(range(len(ri.columns))) }, inplace=True)
        # Rename the first column to 'Fields'
        ri.rename(columns={'0':'Fields' }, inplace=True)
        # Drop columns with all NaN values
        ri = ri.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        ri.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(ri, hide_index=True, use_container_width=True, height=668)

    with tab3:
        # Tab for WP 1
        st.subheader('WP 1')
        # Process rows 38 to 58 in the Exel Sheet and transpose
        wp1 = all_dfs[category][atmp].iloc[:,34:55].T
        # Set the index to the first row
        wp1 = wp1.reset_index()
        # Rename the columns from 0 onwards
        wp1.rename(columns={index : str(value) for index,value in enumerate(range(len(wp1.columns))) }, inplace=True)
        # Rename the first column to 'Fields'
        wp1.rename(columns={'0': 'Fields'}, inplace=True)
        # Drop columns with all NaN values
        wp1 = wp1.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        wp1.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(wp1, hide_index=True, use_container_width=True, height=773)

    with tab4:
        # Tab for Status row 61
        st.subheader(all_dfs[category][atmp].iloc[:,56][1])

