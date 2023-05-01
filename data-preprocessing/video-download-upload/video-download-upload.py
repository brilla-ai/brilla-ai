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
import argparse
import os
from dotenv import load_dotenv


#Brief usage function
def usage():
    print("Usage: python nsmq-video-download-upload.py [options]")
    print("")
    print("Options:")
    print("  --h                  Print this usage message")

#Function to read instruction file containing necessary parameters/values for this script to run
def readInstructionFile():
    load_dotenv()
    with open('ins.json', 'r') as ins:
        data = json.load(ins)
    folder_id = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    folder_name= os.getenv('GOOGLE_DRIVE_NAME')

     # Create a dictionary object with the folder ID and name
    folder_data = {'folder_id': folder_id, 'folder_name': folder_name}
    
    # Update the data object with the folder data
    data.update(folder_data)
    return data

#Function to read excel sheet and return stream/data
def readExcelSheet(doc, sheet):
    df = pd.read_excel(doc, sheet)
    return df

#Function to download video
def downloadVideo(link, localVidDir):
    try:
        yt = YouTube(link)
        video = yt.streams.filter(adaptive=True, file_extension='mp4').order_by('resolution').desc().first()
        video.download(localVidDir)
        print(f"video '{link}' downloaded succesfully")
    except Exception as e:
        print(f'Error downloading {link}: {e}')

#Function to validate json instruction file
def check_json_file(filepath):
    required_keys = ["excel_doc_path", "sheet_name", "video_folder_path", "video_header_name", "service_account_path"]
    
    with open(filepath) as f:
        data = json.load(f)
    
    for key in required_keys:
        if key not in data:
            raise ValueError("Bad JSON instruction file")
    
    return True


def __main__(args):
#Validate Json file and throw error if file is bad
    try:
        check_json_file("ins.json")
        print("JSON file contains all the required keys")
    except ValueError as e:
        print(str(e))

    #read json file
    jsonData = readInstructionFile()

    #Define doc variables
    excelDocumentName = jsonData['excel_doc_path']  #document path
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
        downloadVideo(link, localVideoDirectoryPath)

    # Authenticate with Google Drive API and create a folder to store the videos
    creds = service_account.Credentials.from_service_account_file(serviceAccountFilePath)
    driveService = build('drive', 'v3', credentials=creds)

    #name of local folder to contain donwload videos
    folder_name = jsonData['google_drive_folder_name']

    fileMetaData = {'name': folder_name, 'mimeType': 'video/mp4'}
    folder = driveService.files().create(body=fileMetaData, fields='id').execute()
    folder_id = folder.get('id') #can also be picked up from jsonData
    #folder_id = jsonData['google_drive_folder_ID']

    print(folder_id)


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


#Main program entry point
if __name__ == "__main__":
    with open("README.md", "r") as f:
        description = f.read()

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--h", action="store_true", help=description)
    args = parser.parse_args()

    if args.h:
        usage()
    else:
        __main__(args)
        