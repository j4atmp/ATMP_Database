import pandas as pd
import os
import streamlit as st
import numpy as np
from dataframe_conversion import df_converter

all_dfs = df_converter()

# ATMP Cover Sheet
    # columns 0-11
# Regulatory Information
    # columns 12-30
# WP 1
    # columns 31-51

tab1, tab2, tab3 = st.tabs(['ATMP Cover Sheet', 'Regulatory Information', 'WP 1'])

with tab1:
    st.subheader('ATMP Cover Sheet')
    test = all_dfs['GTMP']['ARI-0001'].iloc[:,0:12].T
    test = test.drop(columns=[2,3,4])
    #test = test.reset_index()
    test.rename(columns={0: 'Fields', 1: 'Values'}, inplace=True)
    st.table(test)
   