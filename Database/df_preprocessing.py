import numpy as np

def data_processing(atmp_fields):
    tmp_df = atmp_fields.copy()
    tmp_df.columns = [f'Values_{i}' for i in range(len(tmp_df.columns))]
    # Rename the first column to 'Fields'
    tmp_df.rename(columns={'Values_0': 'Fields'}, inplace=True)
    # Drop columns with all NaN values
    tmp_df = tmp_df.dropna(axis=1,how='all')
    # Replace NaN values with empty strings
    tmp_df.replace(np.nan, '', inplace=True)

    return tmp_df