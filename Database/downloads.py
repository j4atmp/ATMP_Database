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

# Donwload all ATMPS as CSV 
if formats == 'CSV' and options == 'All':
    # create dirs with all atmps
    if not os.path.isdir('all_dfs_csv'):
        os.makedirs('all_dfs_csv')
    for category in all_dfs.keys():
        for atmp in all_dfs[category]:
            if not os.path.isdir(f'all_dfs_csv/{category}'):
                os.makedirs(f'all_dfs_csv/{category}')
            all_dfs[category][atmp].to_csv(f'all_dfs_csv/{category}/{atmp}.csv', index=False)
    # create Zip
    shutil.make_archive('all_dfs_csv'.replace('.zip', ''), 'zip', 'all_dfs_csv')
    # Donwload zip archive
    with open('all_dfs_csv.zip', 'rb') as f:
        btn_all_dfs_csv = st.download_button(
            label = 'Download all ATMPs as CSV!',
            data = f.read(),
            file_name = 'all_dfs_csv.zip',
            mime ='application/zip'
    )
# Donwload single ATMPS as CSV 
elif formats == 'CSV' and options != 'All' and options != 'sCTMP' and options != 'cATMP':
    # create dir for selected atmp
    for cat in all_dfs.keys():
        if not os.path.isdir(cat):
            os.makedirs(cat)
        for atmp in all_dfs[cat]:
            all_dfs[cat][atmp].to_csv(f'{cat}/{atmp}.csv', index=False)
        # create Zip
        shutil.make_archive(cat.replace('.zip', ''), 'zip', cat)
        # Donwload zip archive
        if options == cat:
            with open(f'{cat}.zip', 'rb') as f:
                btn_all_dfs_csv = st.download_button(
                    label = f'Download all {cat}s as CSV!',
                    data = f.read(),
                    file_name = f'{cat}.zip',
                    mime ='application/zip'
            )
else:
    st.write('Not implemented yet!')
    
