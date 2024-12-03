import streamlit as st

title_page = st.Page("title_page.py", title="Home", icon=":material/home:")
coversheet = st.Page("coversheet.py", title="Coversheet", icon=":material/dataset:")

pg = st.navigation([title_page, coversheet])
st.set_page_config(page_title="Data manager", page_icon=":material/edit:")
pg.run()