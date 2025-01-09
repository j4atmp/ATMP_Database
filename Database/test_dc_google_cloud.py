from google.cloud import storage
from google.auth import load_credentials_from_file
import numpy as np
import pandas as pd
import io
import os
import joblib

def list_bucket_objects(bucket_name, credentials_path):
    """List all objects in the specified Google Cloud Storage bucket."""
    # Load credentials explicitly
    credentials, project = load_credentials_from_file(credentials_path)
    
    # Initialize the client with explicit credentials
    client = storage.Client(credentials=credentials, project=project)
    
    # Access the bucket
    bucket = client.bucket(bucket_name)
    
    # List objects in the bucket
    objects = bucket.list_blobs()
    return [blob.name for blob in objects]

def df_converter():
    bucket_name = 'atmp_coversheets'
    credentials_path = 'google.auth'
    all_files = []

    # get all file_paths in bucket
    if bucket_name and credentials_path:
        print("\nFetching objects from bucket...\n")
        objects = list_bucket_objects(bucket_name, credentials_path)
        
        if objects:
            for obj in objects:
                all_files.append(obj)

        else:
            print("No objects found in this bucket or an error occurred.")
    else:
        print("Bucket name or credentials path cannot be empty.")

    credentials, project = load_credentials_from_file(credentials_path)
    client = storage.Client(credentials=credentials, project=project)
    bucket = client.bucket(bucket_name)
    all_dfs = dict()
    categories = []
    unused_files = []
    all_files_copy = all_files.copy()

    # extract categories from file_paths 
    for file_path in all_files:
        tmp = file_path.split('/')[0]
        if tmp not in categories:
            categories.append(tmp)
    print(categories)
    # create dataframes
    for category in categories:
        if category not in all_dfs.keys():
            all_dfs[category] = dict()
        # update all_files_copy that where not used / are from a different category
        if len(unused_files) > 0:
            all_files_copy = unused_files.copy()
            unused_files.clear()

        # iterate over all_files_copy
        for file in all_files_copy:
            if len(all_files_copy) == 0:
                break
            if category in file:
                blob = bucket.blob(file)
                file_content = blob.download_as_bytes()
                df = pd.read_excel(io.BytesIO(file_content), skiprows=(0, 14, 35), header=None, index_col=0)
                df = df.T
                df = df.drop(columns=np.nan)
                atmp_id = df[df.columns[0]].iloc[0]
                if atmp_id in all_dfs[category].keys():
                    continue
                else:
                    all_dfs[category][atmp_id] = df
            else:
                unused_files.append(file)
            
    return all_dfs


if __name__ == "__main__":
    export = df_converter()
    os.chdir("..")
    joblib.dump(export, 'all_dfs.pkl')
