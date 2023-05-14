#!/usr/bin/env python3

# Import libraries
import sys # System
import whisper  # Speech-to-text
import torch 
from moviepy.editor import VideoFileClip  # Video clipping
import os # Working with directory
import json # Working with JSON
import re # Regular expression
import argparse

# Function to display help text # Add argparse to this as well as a main function
def print_help():
    """
    Print usage instructions
    """
    print("Usage: python crop_riddle_fs.py [OPTIONS]")
    print("")
    print("Options:")
    print("  -h, --help          Display this help message and exit")
    print("  -v, --version       Display the script version and exit")
    print("  -i, --instruction   Provide the path to the instruction file")
    print("")
    print("Usage Instructions:")
    print("- Provide the root path of videos in the instruction file.")
    print("- Provide the destination path of cropped videos in the instruction file.")
    print("- If necessary, configure the target statements in the instruction file.")
    print("- Ensure the videos in the root path end with an mp4 extension.")
    sys.exit(0)

# -------------------------------------------------
# Function to read instruction file root directory
#--------------------------------------------------
def readInstructionFile():
    """
    Read instruction file
    """
    with open('ins.json', 'r') as ins:
        data = json.load(ins)
    return data

# Function to validate json instruction file
def check_json_file(filepath):
    """
    Check required keys inside json file
    """
    required_keys = ["root_path", "cropped_video_destination_path"]

    with open(filepath) as f:
        data = json.load(f)

    for key in required_keys:
        if key not in data:
            raise ValueError("Check required parameters in instruction file")

    return True

# Check json file
print("Checking instruction file...")
check_json_file("ins.json")

# Read instructions from file
data = readInstructionFile() 
    
# Get root path and destination path from instructions
root_path = data["root_path"] 

# Check if root path is absolute
print("Checking if root path provided is an absolute path...")
if not os.path.isabs(root_path):
   raise ValueError("Root path must be an absolute path")

cropped_video_destination_path = data["cropped_video_destination_path"]

# List to provide path(s) of videos to be transcribed
video_paths = [os.path.join(root_path, f) for f in os.listdir(root_path)
               if f.endswith('.mp4')]

#------------------------------------------------------------------
# Destination path
# Create a new directory to store the cropped video and audio files 
# specified in instruction file
#--------------------------------------------------------------------
if not os.path.exists(cropped_video_destination_path):
    os.makedirs(cropped_video_destination_path)
else:
    # Seek permission to go ahead with existing folder
    permission = input(f"Do you want to use the existing folder:\
                       {cropped_video_destination_path}  \
                       for the cropped videos [y or n]: ") 
    if permission.lower() == "y":
        print("Going ahead with the script...")
    else:
        raise ValueError("Please check destination folder of cropped videos in the \
                         instructions file")
 
def __main__(args):
    """
    Entry point of the script
    """   
    # Loop over list of video path
    for i, video_path in enumerate(video_paths):
    
        # Extract file name from video path
        filename = os.path.basename(video_path)
    
        # Remove file extension
        filename = os.path.splitext(filename)[0]
    
        # Video file 
        video = VideoFileClip(video_path) 
    
        # Clip off part of the video
        duration = video.duration
        start_time = duration * 0.78
        end_time = duration * 0.97
        # Retain the remaining of the video
        video = video.subclip(start_time, end_time)
    
        # Make new directory for clipped videos
        if not os.path.exists("temp_videos"):
            os.makedirs("temp_videos")

        # Write clipped videos
        video.write_videofile(f"temp_videos/{filename}.mp4", fps=video.fps) 

        # Check device
        torch.cuda.is_available()
        DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

        # Load whisper model and transcribe
        model = whisper.load_model("base", device=DEVICE)
        print("Transcribing video...")
    
        # Transcribe video
        result = model.transcribe(f"temp_videos/{filename}.mp4")  
    
        # Define default values for cropped video and end segment
        cropped_video = video
        end_segment = end_time

        # Access text, start and end time in the transcribed result
        for segment in result["segments"]:
            # Access text, start and end time in the transcribed result
            text = segment["text"]
            start = segment["start"]
            end = segment["end"]

            # List of target statements to crop on
            target_statements = data["target_statements"]
            for statement in target_statements:
                if re.search(statement, text, re.IGNORECASE):
                    print(f"Start statement: {statement} found at {start} time and \
                           {end} time")
                    # Crop video
                    cropped_video = video.subclip(start)
                    # Stop search when match is found
                    break
                else:
                    print("Start statement not found in text")
            end_segment = end
        # Set end of video 
        cropped_video.set_end(end_segment)
    
        # Save cropped video
        cropped_video.write_videofile(f"{cropped_video_destination_path}/{filename}_cropped.mp4",
                                  fps=video.fps)  
 
if __name__ == "__main__":
    with open("README.md", "r") as f:
        description = f.read()

    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--h", action="store_true", help=description)
    args = parser.parse_args()

    if args.h:
        print_help()
    else:
        __main__(args)  
                