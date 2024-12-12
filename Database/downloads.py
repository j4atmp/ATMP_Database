import streamlit as st

st.title('Download Database')

options = st.selectbox(
    "Options",
    options=('All', 'GTMP', 'TEP', 'sCTMP', 'cATMP'),
    index=None,
    placeholder="Choose an Option"
)

formats = st.selectbox(
    "Format",
    options=('CSV', 'PKL'),
    index=None,
    placeholder="Choose an Option"
)

if formats == 'PKL' and options =='All':
    st.download_button(
        label="Download data as PKL",
        data='/..all_dfs.pkl',
        file_name="ATMPS.pkl",
    )
else:
    st.write('Not implemented yet!')
    
