import streamlit as st
import shutil
import os
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from utilities import data_processing

CHUNK_SIZE = 59
ATMP_CATEGORY = 13 # atmp.iloc[ATMP_CATEGORY][1] == Category_Value
ATMP_ID = 1  # atmp.iloc[ATMP_ID][1] == ID_Value

# connect to Master sheet on Google Drive
conn = st.connection("gsheets", type=GSheetsConnection)
df_master = conn.read()

# load the data
all_dfs = df_master.copy()
# create chunks with size 60
all_dfs_chunks = [all_dfs.iloc[i:i + CHUNK_SIZE] for i in range(0, len(all_dfs), CHUNK_SIZE)]

st.title('Download Database')

options = st.selectbox(
    'Options',
    options=('All', 'GTMP', 'TEP', 'sCTMP', 'cATMP'),
    index=None,
    placeholder='Choose an Option'
)

# Excel
## Donwload all ATMPS as Excel 
if options == 'All':
    # create dirs with all atmps
    if not os.path.isdir('downloads_excel/all_dfs_excel'):
        os.makedirs('downloads_excel/all_dfs_excel')
    for atmp in all_dfs_chunks:
        category = str(atmp.iloc[ATMP_CATEGORY][1])
        if not os.path.isdir(f'downloads_excel/all_dfs_excel/{category}'):
            os.makedirs(f'downloads_excel/all_dfs_excel/{category}')
        # create Excels
        with pd.ExcelWriter(f'downloads_excel/all_dfs_excel/{category}/{atmp.iloc[ATMP_ID][1]}.xlsx') as writer:  
            data_processing(atmp.iloc[1:14]).to_excel(writer, sheet_name='ATMP Cover Sheet', index=False)
            data_processing(atmp.iloc[15:34]).to_excel(writer, sheet_name='Regulatory Information', index=False)
            data_processing(atmp.iloc[35:56]).to_excel(writer, sheet_name='WP 1', index=False)
            data_processing(atmp.iloc[57:,:2]).to_excel(writer, sheet_name='Review Status Information', index=False)
            writer.close()
    # create Zip
    shutil.make_archive('downloads_excel/all_dfs_excel'.replace('.zip', ''), 'zip', 'downloads_excel/all_dfs_excel')
    # Donwload zip archive
    with open('downloads_excel/all_dfs_excel.zip', 'rb') as f:
        btn_all_dfs_excel = st.download_button(
            label = 'Download all ATMPs as Excel',
            data = f.read(),
            file_name = 'All_ATMPs_Excel.zip',
            mime ='application/zip'
    )
    if os.path.isdir('downloads_excel'):
            shutil.rmtree('downloads_excel')
## Donwload single ATMPS as Excel 
elif options != 'All' and options != 'sCTMP' and options != 'cATMP':
    # filter for selected ATMPs
    tmp_atmps = []
    for chunk in all_dfs_chunks:
        if chunk.iloc[ATMP_CATEGORY][1] == options:
            tmp_atmps.append(chunk)

    # create dir for selected atmp
    cat = str(options)
    if not os.path.isdir(f'downloads_excel/{cat}'):
        os.makedirs(f'downloads_excel/{cat}')
    # create Excels    
    for atmp in tmp_atmps:
        with pd.ExcelWriter(f'downloads_excel/{cat}/{atmp.iloc[ATMP_ID][1]}.xlsx') as writer:  
            data_processing(atmp.iloc[1:14]).to_excel(writer, sheet_name='ATMP Cover Sheet', index=False)
            data_processing(atmp.iloc[15:34]).to_excel(writer, sheet_name='Regulatory Information', index=False)
            data_processing(atmp.iloc[35:56]).to_excel(writer, sheet_name='WP 1', index=False)
            data_processing(atmp.iloc[57:,:2]).to_excel(writer, sheet_name='Review Status Information', index=False)
            writer.close()
    # create Zip
    shutil.make_archive(f'downloads_excel/{cat}'.replace('.zip', ''), 'zip', f'downloads_excel/{cat}')
    # Donwload zip archive
    if options == cat:
        with open(f'downloads_excel/{cat}.zip', 'rb') as f:
            btn_all_cat_excel = st.download_button(
                label = f'Download all {cat}s as Excel',
                data = f.read(),
                file_name = f'{cat}_excel.zip',
                mime ='application/zip'
        )
        if os.path.isdir('downloads_excel'):
            shutil.rmtree('downloads_excel')
                
# Not implmented yet!
if options == 'sCTMP' or options == 'cATMP':
    st.write('Not implemented yet!')
    
