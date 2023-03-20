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
import json
import os



#Function to read instruction file containing necessary parameters/values for this script to run
def readInstructionFile():
    with open('ins.json', 'r') as ins:
        data = json.load(ins)
    print(data)
    return data


def readExcelSheet(doc, sheet):
    df = pd.read_excel(doc, sheet)
    return df


def downloadVideo(link):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(localVideoDirectoryPath)
        print(f"video '{link}' downloaded succesfully")
    except Exception as e:
        print(f'Error downloading {link}: {e}')


jsonData = readInstructionFile()

#Define doc variables
excelDocumentName = jsonData['excel_doc_name']  #document name
excelSheetName = jsonData['sheet_name']  #name of sheet in document
videosHeaderName = jsonData['video_header_name'] #name of header of column containing video links
localVideoDirectoryPath = jsonData['video_folder_path'] #path to folder that will contain downloaded videos locally
serviceAccountFilePath = jsonData['service_account_path'] #path to service account file 

#check if local folder exists. !folder_exists? create it: continue
if not os.path.exists(localVideoDirectoryPath):
    os.makedirs(localVideoDirectoryPath)
    print(f"Folder '{localVideoDirectoryPath}' does not exist. Folder created successfully")
else:
    print(f"Folder '{localVideoDirectoryPath}' already exists.")


# Read the Excel sheet and extract video links
df =readExcelSheet(excelDocumentName, excelSheetName)
videoLinks = df[videosHeaderName]

#Loop through list and download each video
for link in videoLinks:
    downloadVideo(link)

# Authenticate with Google Drive API and create a folder to store the videos
creds = service_account.Credentials.from_service_account_file(serviceAccountFilePath)
driveService = build('drive', 'v3', credentials=creds)

#name of local folder to contain donwload videos
folder_name = jsonData['google_drive_folder_name']

fileMetaData = {'name': folder_name, 'mimeType': 'application/vnd.google-apps.folder'}
folder = driveService.files().create(body=fileMetaData, fields='id').execute()
folder_id = folder.get('id') #can also be picked up from jsonData


# Upload the videos to the Google Drive folder
for videoPath in Path(localVideoDirectoryPath).glob('*.mp4'):
    try:
        print(f"Uploading '{videoPath}' from '{localVideoDirectoryPath}'")
        fileMetaData = {'name': videoPath.name, 'parents': [folder_id]}
        media = MediaFileUpload(str(videoPath))
        file = driveService.files().create(body=fileMetaData, media_body=media, fields='id').execute()
        print(f'Successfully uploaded {videoPath} to {folder_name} folder.') 
    except HttpError as error:
        print(f"An error occurred: '{error}' on '{videoPath}'")
