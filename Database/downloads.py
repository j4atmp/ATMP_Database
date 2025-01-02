import streamlit as st
import joblib
import shutil
import os


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

"""
Create Download Files and download options for CSV and Excel
"""
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
            all_dfs[category][atmp].to_csv(f'downloads_csv/all_dfs_csv/{category}/{atmp}.csv', index=False)
    # create Zip
    shutil.make_archive('downloads_csv/all_dfs_csv'.replace('.zip', ''), 'zip', 'downloads_csv/all_dfs_csv')
    # Donwload zip archive
    with open('downloads_csv/all_dfs_csv.zip', 'rb') as f:
        btn_all_dfs_csv = st.download_button(
            label = 'Download all ATMPs as CSV!',
            data = f.read(),
            file_name = 'all_dfs_csv.zip',
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
                btn_all_dfs_csv = st.download_button(
                    label = f'Download all {cat}s as CSV!',
                    data = f.read(),
                    file_name = f'{cat}.zip',
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
            all_dfs[category][atmp].to_excel(f'downloads_excel/all_dfs_excel/{category}/{atmp}.xlsx', index=False)
    # create Zip
    shutil.make_archive('downloads_excel/all_dfs_excel'.replace('.zip', ''), 'zip', 'downloads_excel/all_dfs_excel')
    # Donwload zip archive
    with open('downloads_excel/all_dfs_excel.zip', 'rb') as f:
        btn_all_dfs_excel = st.download_button(
            label = 'Download all ATMPs as Excel!',
            data = f.read(),
            file_name = 'all_dfs_excel.zip',
            mime ='application/zip'
    )
## Donwload single ATMPS as Excel 
elif formats == 'Excel' and options != 'All' and options != 'sCTMP' and options != 'cATMP':
    # create dir for selected atmp
    for cat in all_dfs.keys():
        if not os.path.isdir(f'downloads_excel/{cat}'):
            os.makedirs(f'downloads_excel/{cat}')
        for atmp in all_dfs[cat]:
            all_dfs[cat][atmp].to_excel(f'downloads_excel/{cat}/{atmp}.xlsx', index=False)
        # create Zip
        shutil.make_archive(f'downloads_excel/{cat}'.replace('.zip', ''), 'zip', f'downloads_excel/{cat}')
        # Donwload zip archive
        if options == cat:
            with open(f'downloads_excel/{cat}.zip', 'rb') as f:
                btn_all_dfs_excel = st.download_button(
                    label = f'Download all {cat}s as Excel!',
                    data = f.read(),
                    file_name = f'{cat}.zip',
                    mime ='application/zip'
            )
                
# Not implmented yet!
else:
    st.write('Not implemented yet!')
    
