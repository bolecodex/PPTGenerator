from google.oauth2 import service_account
from googleapiclient.discovery import build
import requests

def download_ppt_from_google_drive(credentials_path, web_view_link, download_path):
    # Extract file ID from webViewLink
    file_id = web_view_link.split('/')[-2]

    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, scopes=['https://www.googleapis.com/auth/drive'])

    # Create a service client
    service = build('drive', 'v3', credentials=credentials)

    # Request file metadata to get the download URL
    file_metadata = service.files().get(fileId=file_id, fields='webViewLink, webContentLink').execute()

    # Check if a webContentLink is available for direct download
    if 'webContentLink' in file_metadata:
        download_url = file_metadata['webContentLink']
    else:
        # If not, construct the download URL
        download_url = f"https://www.googleapis.com/drive/v3/files/{file_id}?alt=media"

    # Download the file
    response = requests.get(download_url, headers={'Authorization': f'Bearer {credentials.token}'})
    if response.status_code == 200:
        with open(download_path, 'wb') as file:
            file.write(response.content)
        print(f'File downloaded successfully to {download_path}')
    else:
        print(f'Failed to download file: {response.content}')

# Example usage
# credentials_path = 'service-account-credentials.json'
# web_view_link = 'https://docs.google.com/presentation/d/1_5oElwmUY1Z7_7GQ56lzB3xdz6NwXRk9/edit?usp=drivesdk&ouid=109567901216249287883&rtpof=true&sd=true'
# download_path = 'Albert_Einstein_Presentation1.pptx'

# download_ppt_from_google_drive(credentials_path, web_view_link, download_path)
