from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_ppt_to_google_drive(credentials_path, file_path, file_name):
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=['https://www.googleapis.com/auth/drive'])

    # Create a service client
    service = build('drive', 'v3', credentials=credentials)

    # Create a media file upload object
    media = MediaFileUpload(file_path, resumable=True)

    # Create a drive file
    file_metadata = {'name': file_name}

    # Execute the upload
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    # Set file permission
    permission = {'type': 'anyone', 'role': 'writer'}
    service.permissions().create(fileId=file['id'], body=permission).execute()

    # Retrieve and return the file's webViewLink
    updated_file = service.files().get(fileId=file['id'], fields='webViewLink').execute()
    return updated_file.get("webViewLink")

# Use the function
credentials_path = 'service-account-credentials.json'  # Replace with your path
file_path = 'Albert_Einstein_Presentation.pptx'                # Replace with your file path and extension
file_name = 'Albert_Einstein_Presentation.pptx'              # Replace with your file name

webViewLink = upload_ppt_to_google_drive(credentials_path, file_path, file_name)
print(f'File URL: {webViewLink}')