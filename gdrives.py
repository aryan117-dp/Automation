import os
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import io

# Use the same SCOPES you used for Sheets/Gmail
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/gmail.send'
]

def get_drive_service():
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        return build('drive', 'v3', credentials=creds)
    else:
        print("Error: token.json not found. Run your authentication script first.")
        return None

def download_file(self, file_id, destination_path):
        """Downloads a specific file by ID to a local path."""
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Download Progress: {int(status.progress() * 100)}%")
        print(f"File saved to: {destination_path}")

def create_folder(service, folder_name):
    """Creates a folder and returns the folder ID."""
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    try:
        file = service.files().create(body=file_metadata, fields='id').execute()
        print(f"Folder Created! ID: {file.get('id')}")
        return file.get('id')
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None

def upload_file(service, file_path, folder_id=None):
    """Uploads a file to a specific folder."""
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    
    if folder_id:
        file_metadata['parents'] = [folder_id]

    # Change mimetype based on your file (e.g., 'image/jpeg' or 'application/pdf')
    media = MediaFileUpload(file_path, resumable=True)

    try:
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        print(f"File Uploaded! File ID: {file.get('id')}")
    except HttpError as error:
        print(f"An error occurred: {error}")

def list_files(service, limit=10):
    """Lists the most recent files."""
    results = service.files().list(
        pageSize=limit, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
    else:
        print('Recent Files:')
        for item in items:
            print(f"{item['name']} ({item['id']})")

if __name__ == '__main__':
    drive_service = get_drive_service()
    
    if drive_service:
        # 1. List files
        list_files(drive_service)
        
        # 2. Create a backup folder
        #new_folder_id = create_folder(drive_service, "Python_Automated_Backups")
        
        # 3. Upload a test file (Ensure 'test.txt' exists in your directory)
        #with open("test.txt", "w") as f: f.write("Hello Drive!")
        #upload_file(drive_service, "gdrives.py", '10tUVYNlwVoKE3VhFklxe5BZ98PPx5syu')
