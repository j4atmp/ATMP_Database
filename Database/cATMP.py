import streamlit as st
import joblib
from coversheet import coversheet_creator

st.title('cATMP')

st.write('Nothing here yet!')

# all_dfs = joblib.load('../all_dfs.pkl')

# all_cATMPs = list(all_dfs['cATMP'].keys())
# all_cATMPs.sort()

# option = st.selectbox(
#     "cATMP List",
#     options=all_cATMPs,
#     index=None,
#     placeholder="Choose an ATMP"
# )

# for i in all_cATMPs:
#     if option == i:
#         coversheet_creator(all_dfs, category='cATMP', atmp=i)
