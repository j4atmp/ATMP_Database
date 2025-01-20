import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive"]

DOWNLOAD_FOLDER = "../ATMP Sheets"

def authenticate_drive():
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "google_drive_secrets.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds

def get_folder_id(service, parent_folder_name, folder_name):
    query = f"mimeType='application/vnd.google-apps.folder' and name='{folder_name}'"
    parent_results = service.files().list(q=f"mimeType='application/vnd.google-apps.folder' and name='{parent_folder_name}'", fields="files(id, name)").execute()
    parent_folders = parent_results.get("files", [])
    if not parent_folders:
        return None
    parent_id = parent_folders[0]['id']
    results = service.files().list(q=f"'{parent_id}' in parents and name='{folder_name}'", fields="files(id, name)").execute()
    folders = results.get("files", [])
    return folders[0]['id'] if folders else None

def download_google_sheets(service, parent_folder_name, subfolder_name):
    folder_id = get_folder_id(service, parent_folder_name, subfolder_name)
    if not folder_id:
        print(f"Folder '{subfolder_name}' not found inside '{parent_folder_name}'.")
        return

    folder_path = os.path.join(DOWNLOAD_FOLDER, subfolder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    query = f"'{folder_id}' in parents and mimeType='application/vnd.google-apps.spreadsheet'"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get("files", [])
    
    if not files:
        print(f"No Google Sheets found in '{subfolder_name}'.")
        return

    for file in files:
        file_id = file['id']
        file_name = file['name'] + ".xlsx"
        request = service.files().export_media(fileId=file_id, mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        file_path = os.path.join(folder_path, file_name)
        with open(file_path, "wb") as f:
            f.write(request.execute())
        print(f"Downloaded: {file_name} to {folder_path}")
from googleapiclient.http import MediaIoBaseDownload

def main():
    creds = authenticate_drive()
    try:
        service = build("drive", "v3", credentials=creds)
        download_google_sheets(service, "ATMP Sheets", "GTMP")
        download_google_sheets(service, "ATMP Sheets", "TEP")
    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
    print("Download complete.")
    os.chdir("..")
    print("Converting to DataFrame...")
    command = "python dataframe_conversion.py"
    os.system(command)  