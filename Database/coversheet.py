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
    st.title(atmp, anchor=None, help=None)

    # Donwload option as Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
        all_dfs[category][atmp].iloc[:,0:12].T.to_excel(writer, sheet_name='ATMP Cover Sheet')
        all_dfs[category][atmp].iloc[:,12:30].T.to_excel(writer, sheet_name='Regulatory Information')
        all_dfs[category][atmp].iloc[:,31:].T.to_excel(writer, sheet_name='WP 1')
        writer.close()
        btn_single = st.download_button(
                label = 'Download as Excel',
                data = buffer,
                file_name = f'{atmp}.xlsx',
                mime='application/vnd.ms-excel'
        )

    # Cover Sheet Tabs
    tab1, tab2, tab3 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1'])

    with tab1:
        st.subheader('ATMP Cover Sheet')
        test = all_dfs[category][atmp].iloc[:,0:12].T
        
        test = test.reset_index()
        test.rename(columns={index : str(value) for index,value in enumerate(range(len(test.columns))) }, inplace=True)
        test.rename(columns={'0': 'Fields', 1: 'Values'}, inplace=True)
        test = test.dropna(axis=1,how='all')
        test.replace(np.nan, '', inplace=True)
        st.dataframe(test, hide_index=True, use_container_width=True, height=458)

    with tab2:
        st.subheader('Regulatory Information')
        test2 = all_dfs[category][atmp].iloc[:,12:30].T
        test2 = test2.reset_index()
        test2.rename(columns={index : str(value) for index,value in enumerate(range(len(test2.columns))) }, inplace=True)
        test2.rename(columns={'0':'Fields' }, inplace=True)
        test2 = test2.dropna(axis=1,how='all')
        test2.replace(np.nan, '', inplace=True)
        st.dataframe(test2, hide_index=True, use_container_width=True, height=668)

    with tab3:
        st.subheader('WP 1')
        test3 = all_dfs[category][atmp].iloc[:,31:].T
        test3 = test3.reset_index()
        test3.rename(columns={index : str(value) for index,value in enumerate(range(len(test3.columns))) }, inplace=True)
        test3.rename(columns={'0': 'Fields'}, inplace=True)
        test3 = test3.dropna(axis=1,how='all')
        test3.replace(np.nan, '', inplace=True)
        st.dataframe(test3, hide_index=True, use_container_width=True, height=773)

