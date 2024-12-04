import streamlit as st



title_page = st.Page("title_page.py", title="Home", icon=":material/home:")
gtmp = st.Page("gtmp.py", title="GTMP", icon=":material/dataset:")
tep = st.Page("tep.py", title="TEP", icon=":material/dataset:")

pg = st.navigation([title_page, gtmp, tep])
st.set_page_config(page_title="ATMP Database", page_icon=":material/menu:")
pg.run()