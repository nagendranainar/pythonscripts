import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# Function to download file from Zoom
def download_zoom_file(file_id, token):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    url = f"https://api.zoom.us/v2/files/{file_id}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        file_data = response.json()
        download_url = file_data["download_url"]
        file_name = file_data["filename"]

        # Download the file
        response = requests.get(download_url)

        if response.status_code == 200:
            with open(file_name, "wb") as file:
                file.write(response.content)
            return file_name
        else:
            print("Failed to download the file.")
    else:
        print("Failed to retrieve file information from Zoom.")

# Function to upload file to Google Drive
def upload_to_google_drive(file_path, folder_id):
    gauth = GoogleAuth()
    drive = GoogleDrive(gauth)

    # Create a Google Drive file instance
    file = drive.CreateFile({
        'title': file_path.split("/")[-1],
        'parents': [{'id': folder_id}]
    })

    # Set the content of the file
    file.SetContentFile(file_path)

    # Upload the file to Google Drive
    file.Upload()

    print("File uploaded successfully!")

# Zoom API access token
zoom_token = "YOUR_ZOOM_API_TOKEN"

# Google Drive folder ID
folder_id = "YOUR_GOOGLE_DRIVE_FOLDER_ID"

# Zoom file ID (you can find this from the Zoom API or UI)
file_id = "YOUR_ZOOM_FILE_ID"

# Download the file from Zoom
downloaded_file_path = download_zoom_file(file_id, zoom_token)

# Upload the file to Google Drive
upload_to_google_drive(downloaded_file_path, folder_id)
