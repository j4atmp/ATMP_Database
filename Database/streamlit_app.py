import streamlit as st

st.set_page_config(layout="centered",page_title="ATMP Database", page_icon=":material/menu:")


title_page = st.Page("pages/title_page.py", title="Home", icon=":material/home:")
help_page = st.Page("pages/help_page.py", title="Help", icon=":material/help:")
# atmps
dashboard = st.Page("pages/atmps/dashboard.py", title="Dashboard", icon=":material/toolbar:")
gtmp = st.Page("pages/atmps/gtmp.py", title="GTMP", icon=":material/dataset:")
tep = st.Page("pages/atmps/tep.py", title="TEP", icon=":material/dataset:")
sCTMP = st.Page("pages/atmps/sCTMP.py", title="sCTMP", icon=":material/dataset:")
cATMP = st.Page("pages/atmps/cATMP.py", title="cATMP", icon=":material/dataset:")
# tools
search_page = st.Page("pages/tools/search_page.py", title="Search", icon=":material/search:")
download_page = st.Page("pages/tools/downloads.py", title="Download", icon=":material/download:")
upload_page = st.Page("pages/uploads.py", title="Upload", icon=":material/upload:")

pg = st.navigation(
    {
    'Home' : [title_page,help_page],
    'ATMPs' : [dashboard, gtmp, tep, sCTMP, cATMP],
    'Tools': [search_page, download_page,upload_page]
    }
)
pg.run()