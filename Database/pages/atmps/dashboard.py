import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

CHUNK_SIZE = 59
ATMP_CATEGORY = 13 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

# Get Last modification of Master Sheet
# Load secrets
secrets = st.secrets["gsheets"]
# Create credentials from secrets
creds = Credentials.from_service_account_info(secrets)
# Initialize Google Drive API
service = build("drive", "v3", credentials=creds)
# Replace with your Google Sheet file ID
FILE_ID = st.secrets["File_ID"]
# Get file metadata (including last modified time)
file_metadata = service.files().get(fileId=FILE_ID, fields="modifiedTime").execute()



# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

st.title('Overview')

statistics = {'Amount of ATMPs' : {'GTMP' : 0,
                                   'TEP' : 0,
                                   'sCTMP' : 0,
                                   'cATMP' : 0,
                                   'TOTAL' : 0
                                    }
              }

for chunk in all_dfs_chunks:
    statistics['Amount of ATMPs']['TOTAL'] += 1
    if chunk.iloc[ATMP_CATEGORY][1] == 'GTMP':
        statistics['Amount of ATMPs']['GTMP'] += 1
    elif chunk.iloc[ATMP_CATEGORY][1] == 'TEP':
        statistics['Amount of ATMPs']['TEP'] += 1
    elif chunk.iloc[ATMP_CATEGORY][1] == 'sCTMP':
        statistics['Amount of ATMPs']['sCTMP'] += 1
    elif chunk.iloc[ATMP_CATEGORY][1] == 'cATMP':
        statistics['Amount of ATMPs']['cATMP'] += 1

atmps_df = pd.DataFrame.from_dict(statistics['Amount of ATMPs'], orient='index')


st.subheader(f"Number of ATMPs in Database : {statistics['Amount of ATMPs']['TOTAL']}")
st.write("Last update: ", file_metadata["modifiedTime"].split('T')[0])
st.bar_chart(atmps_df.iloc[0:4], horizontal=True)
