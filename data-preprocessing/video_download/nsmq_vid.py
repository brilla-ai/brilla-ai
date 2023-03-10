#This python script reads video links from a given sheet in an excel document, 
#downloads the videos and saves the videos to a google drive folder
#K.T Yeboah | 27-02-2023| 11:44am


#import relevant libaries
import pandas as pd
from pytube import YouTube
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from pathlib import Path


#Define doc variables
excel_document_name = 'NSMQ.xlsx'  #document name
excel_sheet_name = 'Sheet1'   #name of sheet in document
videos_header_name = 'Links' #name of header of column containing video links

# Read the Excel sheet and extract video links
df = pd.read_excel(excel_document_name, excel_sheet_name)
video_links = df[videos_header_name]


# Download videos and save them to a local directory
local_directory = 'videos/'

for link in video_links:
    try:
        yt = YouTube(link)
        video = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(local_directory)
    except Exception as e:
        print(f'Error downloading {link}: {e}')


# Authenticate with Google Drive API and create a folder to store the videos
creds = service_account.Credentials.from_service_account_file('credentials.json')

drive_service = build('drive', 'v3', credentials=creds)

#name of local folder to contain donwloade videos
folder_name = 'NSMQ Video Folder'

file_metadata = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
folder = drive_service.files().create(body=file_metadata, fields='id').execute()
folder_id = folder.get('id')


# Upload the videos to the Google Drive folder
for video_path in Path(local_directory).glob('*.mp4'):
    try:
        file_metadata = {'name': video_path.name, 'parents': [folder_id]}
        media = MediaFileUpload(str(video_path))
        file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f'Successfully uploaded {video_path} to {folder_name} folder.')
    except HttpError as error:
        print(f'An error occurred: {error}')
