import os
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

class GoogleDriveService:
    def __init__(self):
        # This assumes credentials.json or client_secrets.json is available
        # or that settings.yaml is configured for service account/OAuth
        self.drive = None
        self._authenticate()

    def _authenticate(self):
        try:
            gauth = GoogleAuth()
            # Try to load saved client credentials
            gauth.LocalWebserverAuth() 
            self.drive = GoogleDrive(gauth)
        except Exception as e:
            print(f"GDrive Auth failed: {e}. Falling back to internal storage only.")

    def upload_to_folder(self, folder_name, file_name, local_path):
        if not self.drive:
            return None
        
        # 1. Find or create folder
        query = f"title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        file_list = self.drive.ListFile({'q': query}).GetList()
        
        if file_list:
            folder_id = file_list[0]['id']
        else:
            folder = self.drive.CreateFile({'title': folder_name, 'mimeType': 'application/vnd.google-apps.folder'})
            folder.Upload()
            folder_id = folder['id']

        # 2. Upload file
        file_drive = self.drive.CreateFile({
            'title': file_name,
            'parents': [{'id': folder_id}]
        })
        file_drive.SetContentFile(local_path)
        file_drive.Upload()
        return file_drive['alternateLink']

gdrive_service = GoogleDriveService()
