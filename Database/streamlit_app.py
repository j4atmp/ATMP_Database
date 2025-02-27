import streamlit as st

title_page = st.Page("pages/title_page.py", title="Home", icon=":material/home:")

# pages
gtmp = st.Page("pages/gtmp.py", title="GTMP", icon=":material/dataset:")
tep = st.Page("pages/tep.py", title="TEP", icon=":material/dataset:")
sCTMP = st.Page("pages/sCTMP.py", title="sCTMP", icon=":material/dataset:")
cATMP = st.Page("pages/cATMP.py", title="cATMP", icon=":material/dataset:")
# Divers
search_page = st.Page("pages/search_page.py", title="Search", icon=":material/search:")
download_page = st.Page("pages/downloads.py", title="Download", icon=":material/download:")
help_page = st.Page("pages/help_page.py", title="Help", icon=":material/help:")
upload_page = st.Page("pages/uploads.py", title="Upload", icon=":material/upload:")

pg = st.navigation([title_page, gtmp, tep, sCTMP, cATMP, search_page, download_page,upload_page, help_page])
st.set_page_config(page_title="ATMP Database", page_icon=":material/menu:")
pg.run()