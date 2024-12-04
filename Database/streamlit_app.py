import streamlit as st

title_page = st.Page("title_page.py", title="Home", icon=":material/home:")

# ATMPs
gtmp = st.Page("gtmp.py", title="GTMP", icon=":material/dataset:")
tep = st.Page("tep.py", title="TEP", icon=":material/dataset:")
sCTMP = st.Page("sCTMP.py", title="sCTMP", icon=":material/dataset:")
cATMP = st.Page("cATMP.py", title="cATMP", icon=":material/dataset:")
# Divers
download_page = st.Page("downloads.py", title="Download", icon=":material/download:")
help_page = st.Page("help_page.py", title="Help", icon=":material/help:")

pg = st.navigation([title_page, gtmp, tep, sCTMP, cATMP, download_page, help_page])
st.set_page_config(page_title="ATMP Database", page_icon=":material/menu:")
pg.run()