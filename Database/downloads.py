import streamlit as st
import joblib
import shutil
import os
import pandas as pd


all_dfs = joblib.load('../all_dfs.pkl')


st.title('Download Database')

options = st.selectbox(
    'Options',
    options=('All', 'GTMP', 'TEP', 'sCTMP', 'cATMP'),
    index=None,
    placeholder='Choose an Option'
)

formats = st.selectbox(
    'Format',
    options=('CSV', 'Excel'),
    index=None,
    placeholder='Choose an Option'
)

# CSV
## Donwload all ATMPS as CSV 
if formats == 'CSV' and options == 'All':
    # create dirs with all atmps
    if not os.path.isdir('downloads_csv/all_dfs_csv'):
        os.makedirs('downloads_csv/all_dfs_csv')
    for category in all_dfs.keys():
        for atmp in all_dfs[category]:
            if not os.path.isdir(f'downloads_csv/all_dfs_csv/{category}'):
                os.makedirs(f'downloads_csv/all_dfs_csv/{category}')
            all_dfs[category][atmp].to_csv(f'downloads_csv/all_dfs_csv/{category}/{atmp}.csv')
    # create Zip
    shutil.make_archive('downloads_csv/all_dfs_csv'.replace('.zip', ''), 'zip', 'downloads_csv/all_dfs_csv')
    # Donwload zip archive
    with open('downloads_csv/all_dfs_csv.zip', 'rb') as f:
        btn_all_dfs_csv = st.download_button(
            label = 'Download all ATMPs as CSV',
            data = f.read(),
            file_name = 'All_ATMPs_CSV.zip',
            mime ='application/zip'
    )
## Donwload single ATMPS as CSV 
elif formats == 'CSV' and options != 'All' and options != 'sCTMP' and options != 'cATMP':
    # create dir for selected atmp
    for cat in all_dfs.keys():
        if not os.path.isdir(f'downloads_csv/{cat}'):
            os.makedirs(f'downloads_csv/{cat}')
        for atmp in all_dfs[cat]:
            all_dfs[cat][atmp].to_csv(f'downloads_csv/{cat}/{atmp}.csv', index=False)
        # create Zip
        shutil.make_archive(f'downloads_csv/{cat}'.replace('.zip', ''), 'zip', f'downloads_csv/{cat}')
        # Donwload zip archive
        if options == cat:
            with open(f'downloads_csv/{cat}.zip', 'rb') as f:
                btn_all_cat_csv = st.download_button(
                    label = f'Download all {cat}s as CSV',
                    data = f.read(),
                    file_name = f'{cat}_csv.zip',
                    mime ='application/zip'
            )

# Excel
## Donwload all ATMPS as Excel 
if formats == 'Excel' and options == 'All':
    # create dirs with all atmps
    if not os.path.isdir('downloads_excel/all_dfs_excel'):
        os.makedirs('downloads_excel/all_dfs_excel')
    for category in all_dfs.keys():
        for atmp in all_dfs[category]:
            if not os.path.isdir(f'downloads_excel/all_dfs_excel/{category}'):
                os.makedirs(f'downloads_excel/all_dfs_excel/{category}')
            # create Excels
            with pd.ExcelWriter(f'downloads_excel/all_dfs_excel/{category}/{atmp}.xlsx') as writer:  
                all_dfs[category][atmp].iloc[:,0:12].T.to_excel(writer, sheet_name='ATMP Cover Sheet')
                all_dfs[category][atmp].iloc[:,12:30].T.to_excel(writer, sheet_name='Regulatory Information')
                all_dfs[category][atmp].iloc[:,31:].T.to_excel(writer, sheet_name='WP 1')
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
## Donwload single ATMPS as Excel 
elif formats == 'Excel' and options != 'All' and options != 'sCTMP' and options != 'cATMP':
    # create dir for selected atmp
    for cat in all_dfs.keys():
        if not os.path.isdir(f'downloads_excel/{cat}'):
            os.makedirs(f'downloads_excel/{cat}')
        # create Excels    
        for atmp in all_dfs[cat]:
            with pd.ExcelWriter(f'downloads_excel/{cat}/{atmp}.xlsx') as writer:  
                all_dfs[cat][atmp].iloc[:,0:12].T.to_excel(writer, sheet_name='ATMP Cover Sheet')
                all_dfs[cat][atmp].iloc[:,12:30].T.to_excel(writer, sheet_name='Regulatory Information')
                all_dfs[cat][atmp].iloc[:,31:].T.to_excel(writer, sheet_name='WP 1')
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
                
# Not implmented yet!
if options == 'sCTMP' or options == 'cATMP':
    st.write('Not implemented yet!')
    
