import streamlit as st
import joblib
from coversheet import coversheet_creator

st.title('sCTMP')

st.write('Nothing here yet!')

# all_dfs = joblib.load('../all_dfs.pkl')

# all_sCTMPs = list(all_dfs['sCTMP'].keys())
# all_sCTMPs.sort()

# option = st.selectbox(
#     "sCTMP List",
#     options=all_sCTMPs,
#     index=None,
#     placeholder="Choose an ATMP"
# )

# for i in all_sCTMPs:
#     if option == i:
#         coversheet_creator(all_dfs, category='sCTMP', atmp=i)