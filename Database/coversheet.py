import streamlit as st
import joblib
# from dataframe_conversion import df_converter

# all_dfs = df_converter()
all_dfs = joblib.load('../all_dfs.pkl')

# ATMP Cover Sheet
    # columns 0-11
# Regulatory Information
    # columns 12-30
# WP 1
    # columns 31-51

# ATMPs
st.title('ARI-0001', anchor=None, help=None)
# Cover Sheets
tab1, tab2, tab3 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1'])

with tab1:
    st.subheader('ATMP Cover Sheet')
    test = all_dfs['GTMP']['ARI-0001'].iloc[:,0:12].T
    test = test.drop(columns=[2,3,4])
    test = test.reset_index()
    test.rename(columns={0: 'Fields', 1: 'Values'}, inplace=True)
    st.dataframe(test, hide_index=True, use_container_width=True, height=458)

with tab2:
    st.subheader('Regulatory Information')
    test2 = all_dfs['GTMP']['ARI-0001'].iloc[:,12:30].T
    test2 = test2.reset_index()
    test2.rename(columns={index : str(value) for index,value in enumerate(range(len(test2.columns))) }, inplace=True)
    test2.rename(columns={'0':'Fields' }, inplace=True)
    st.dataframe(test2, hide_index=True, use_container_width=True, height=668)

with tab3:
    st.subheader('WP 1')
    test3 = all_dfs['GTMP']['ARI-0001'].iloc[:,31:].T
    test3 = test3.drop(columns=[2,3,4])
    test3 = test3.reset_index()
    test3.rename(columns={0: 'Fields', 1: 'Anwsers'}, inplace=True)
    st.dataframe(test3, hide_index=True, use_container_width=True, height=773)