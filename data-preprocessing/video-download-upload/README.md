'This python script reads video links from a given sheet in an excel document, 
downloads the videos and saves the videos to a google drive folder
K.T Yeboah | 27-02-2023| 11:44am

The instruction file (ins.json file) contains input variable parameters necessary to run the script.
Note that the ins file should be in the same directory as this script. Google drive folder name and ID should be stored in a .env file
To run the script, first set the necesary parameters in the instruction file (ins.json) and save.
The credentials.json file is a service file containing API keys, IDs and authorization credentials to the google drive folder in use. 
To obtain a service file that points to a particular google drive folder, visit google cloud storage console (https://cloud.google.com/)
Thereafter, invoke the python interpretor on the command line and add the name of the script=> py nsmq_vid.py'