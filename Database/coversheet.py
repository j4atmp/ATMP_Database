import streamlit as st
import numpy as np
import os
import io
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

ATMP_ID = 1 # atmp.iloc[ATMP_ID][1] == ID_Value

def coversheet_creator(atmp, category):
# ATMP Cover Sheet
    # columns 0-11
# Regulatory Information
    # columns 12-30
# WP 1
    # columns 31-51

    # selected ATMP
    st.title(atmp.iloc[ATMP_ID][1])

    # # Donwload option as Excel
    # buffer = io.BytesIO()
    # with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
    #     all_dfs[category][atmp].iloc[:,0:13].T.to_excel(writer, sheet_name='ATMP Cover Sheet')
    #     all_dfs[category][atmp].iloc[:,14:33].T.to_excel(writer, sheet_name='Regulatory Information')
    #     all_dfs[category][atmp].iloc[:,34:55].T.to_excel(writer, sheet_name='WP 1')
    #     all_dfs[category][atmp].iloc[:,56].T.to_excel(writer, sheet_name='Status Information')
    #     writer.close()
    #     btn_single = st.download_button(
    #             label = 'Download as Excel',
    #             data = buffer,
    #             file_name = f'{atmp}.xlsx',
    #             mime='application/vnd.ms-excel'
    #     )

    # Cover Sheet Tabs
    tab1, tab2, tab3, tab4 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1', 'Review Status Information'])

    with tab1:
        # Tab for ATMP Cover Sheet
        st.subheader('ATMP Cover Sheet')
        # Process rows 1 to 13 in the atmp dataframe
        cs = atmp.iloc[1:14]
        # Generate new column names dynamically
        cs.columns = [f'Values_{i}' for i in range(len(cs.columns))]
        # Rename the first column to 'Fields'
        cs.rename(columns={'Values_0': 'Fields'}, inplace=True)
        # Drop columns with all NaN values
        cs = cs.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        cs.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(cs, hide_index=True, use_container_width=True, height=458)

    with tab2:
        # Tab for Regulatory Information
        st.subheader('Regulatory Information')
        # Process rows 16 to 34 in the atmp dataframe
        ri = atmp.iloc[16:35]
        # Generate new column names dynamically
        ri.columns = [f'Values_{i}' for i in range(len(ri.columns))]
        # Rename the first column to 'Fields'
        ri.rename(columns={'Values_0': 'Fields'}, inplace=True)
        # Drop columns with all NaN values
        ri = ri.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        ri.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(ri, hide_index=True, use_container_width=True, height=668)

    with tab3:
        # Tab for WP 1
        st.subheader('WP 1')
        # Process rows 38 to 56 in the atmp dataframe
        wp1 = atmp.iloc[36:57]
       # Generate new column names dynamically
        wp1.columns = [f'Values_{i}' for i in range(len(wp1.columns))]
        # Rename the first column to 'Fields'
        wp1.rename(columns={'Values_0': 'Fields'}, inplace=True)
        # Drop columns with all NaN values
        wp1 = wp1.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        wp1.replace(np.nan, '', inplace=True)
        # Display the dataframe
        st.dataframe(wp1, hide_index=True, use_container_width=True, height=773)

    with tab4:
        # Tab for Review Status Information
        st.subheader('Review Status Information')
        # Process rows 58 and 59 in the atmp dataframe
        rs = atmp.iloc[58:,:2]
        # Generate new column names dynamically
        rs.columns = [f'Values_{i}' for i in range(len(rs.columns))]
        # Rename the first column to 'Fields'
        rs.rename(columns={'Values_0': 'Fields'}, inplace=True)
        # Drop columns with all NaN values
        rs = rs.dropna(axis=1,how='all')
        # Replace NaN values with empty strings
        rs.replace(np.nan, '', inplace=True)
        st.dataframe(rs, hide_index=True)

