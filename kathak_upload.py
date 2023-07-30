from __future__ import print_function

import os.path
import requests

from pprint import pprint

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


def download_file(url, save_path):
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        pprint("File downloaded successfully.")
    else:
        pprint("Failed to download the file.")

# Example usage
zoom_file_url = "https://zoom.us/sample-file.pdf"
save_file_path = "path/to/save/sample-file.pdf"
download_file(zoom_file_url, save_file_path)

zoom_file_name = 'GMT20230606-221927_Recording_640x360-copy.mp4'

SCOPES = ['https://www.googleapis.com/auth/drive']

loginCredit = None


downloadPath = '/Users/naikumar/Downloads/'
zoomFilePath = os.path.join(downloadPath + zoom_file_name)
#zoomFileName = '/Users/naikumar/Downloads/GMT20230606-221927_Recording_640x360-copy.mp4'
FileName = zoomFilePath.split("/")[-1]
googleDriveFolder = '1V7LY8VSX14JJZjOwfKXXkWRHHinkNDYn'

file_metadata = {
    "name": FileName,
    "parents": [googleDriveFolder]
}

if os.path.exists('token.json'):
    loginCredit = Credentials.from_authorized_user_file('token.json', SCOPES)
if not loginCredit or not loginCredit.valid:
    if loginCredit and loginCredit.expired and loginCredit.refresh_token:
        loginCredit.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        loginCredit = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(loginCredit.to_json())

service = build('drive', 'v3', credentials=loginCredit)

#Media File Upload

media = MediaFileUpload(zoomFilePath)

file = service.files().create(
    body=file_metadata, 
    media_body=media, 
    fields='id').execute()
