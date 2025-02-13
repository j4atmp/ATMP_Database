import streamlit as st
import pandas as pd
import io
from streamlit_gsheets import GSheetsConnection
from utilities import check_password, upload_atmp, update_atmp

CHUNK_SIZE = 60
ATMP_CATEGORY = 14 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value
file = 'Database/pages/ATMP_Cover_Sheet_Template.xlsx'
# template = pd.read_excel(file, header=None)

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()
# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

st.title('Upload ATMP-Sheet')
# load the data

st.markdown(
    """
    For uploading/updating ATMP-Sheets you should be member of WP1   
    If you are not member of WP1, there are two options:
    
    - Send your ATMP information (in Template Excel format) to j4atmp@gmail.com
    - or send an Email to j4atmp@gmail.com. to recive login access

    *State your institute affiliation in your email
    
    **:red[Please always use the Template Format and do not change it!!!]**
    
    """
    )

# create list of current ATMP IDs
Current_Atmps = []
for chunk in all_dfs_chunks:
    if chunk.iloc[ATMP_ID][1] not in Current_Atmps:
        Current_Atmps.append(chunk.iloc[ATMP_ID][1])
# sort list of current ATMP IDs
Current_Atmps.sort()
template = all_dfs_chunks[0]

st.subheader('Cover Sheet Example (as Template)')

#st.markdown('''
#    - For uploading new ATMPs we suggest to download and use the **Template Excel file**.
#    - For updating exsiting ATMPs we suggest to download the current specific **ATMP Excel Template** from the Database.
#    ''')

@st.dialog("Select")
def vote1():
    option = st.selectbox(
        "GTMP List",
        options=Current_Atmps,
        index=None,
        placeholder="Choose an ATMP"
    )
    if option:
        for chunk in all_dfs_chunks:
            if chunk.iloc[ATMP_ID][1] == option:
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    chunk.to_excel(writer, index=False, header=False)
                    writer.close()
                    st.download_button(
                            label = 'Download as Excel',
                            data = buffer,
                            file_name = f'{option}.xlsx',
                            mime='application/vnd.ms-excel'
                    )

col1, col2 = st.columns(2)

with col1:
    with open(file, 'rb') as my_file:
        st.download_button(label = ':arrow_down: Download Template Excel file', 
        data = my_file, 
        file_name = 'ATMP_Cover_Sheet_Template.xlsx', 
        mime = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    st.markdown('''For uploading new ATMPs:

    1. Download the **Template Excel file**
    2. Edit template file contents according to new ATMP
    3. Upload the new ATMP Excel file

    ''')

with col2:
    if "vote1" not in st.session_state:
        if st.button(':arrow_down: ATMP Templates in Database'):
            vote1()
    st.markdown('''For updating exsiting ATMPs:

    1. Download the **specific** ATMP Excel file from the database 
    2. Edit the specific ATMP Excel file
    3. Upload edited Excel file below

    ''')

        
# Check for WP1 User
if not check_password():
    st.stop()

st.subheader('Upload Options')

#st.markdown('''
#    - For uploading new ATMPs please use the **Upload** button.
#    - For updating exsiting ATMPs please use the **Update** button.
#    ''')

@st.dialog("Select")
def vote2(item):
    uploaded_files = st.file_uploader(
        "Choose an ATMP in the right Format (see Cover Sheet Example)", 
        accept_multiple_files=True,
        type = 'xlsx'
        )
    if item == 'A':
        upload_atmp(uploaded_files, Current_Atmps, all_dfs, template, conn)
    if item == 'B':
        update_atmp(uploaded_files, Current_Atmps, all_dfs, all_dfs_chunks, template, conn)

col3, col4 = st.columns(2)

if "vote2" not in st.session_state:
    with col3:
        if st.button(':arrow_up: Upload new ATMP'):
            vote2('A')
        st.markdown('''To upload **new** ATMP''')

    with col4:
        if st.button(':arrow_up: Update ATMP'):
            vote2('B')
        st.markdown('''To *update* exsiting ATMP''')


