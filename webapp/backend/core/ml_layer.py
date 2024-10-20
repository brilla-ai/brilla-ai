import requests
from pydub import AudioSegment
import os
import math
import base64
import json
import yt_dlp
import tempfile
import subprocess
import os 
import sys
import glob
import re
import time


current_round = 4

# Function to split audio into chunks and transcribe them
def transcribe_in_chunks(audio_path: str, base_url: str, chunk_duration_ms: int = 10000):
    audio = AudioSegment.from_file(audio_path)
    total_duration_ms = len(audio)  # Get the total duration in milliseconds
    num_chunks = math.ceil(total_duration_ms / chunk_duration_ms)
    
    transcript = ""
    
    for i in range(num_chunks):
        start_time = i * chunk_duration_ms
        end_time = min(start_time + chunk_duration_ms, total_duration_ms)
        
        # Extract chunk of audio
        audio_chunk = audio[start_time:end_time]
        
        # Save chunk as temporary file
        chunk_path = f"chunk_{i}.wav"
        audio_chunk.export(chunk_path, format="wav")
        
        # Transcribe chunk
        chunk_transcript = transcribe_audio_chunk(chunk_path, base_url)
        transcript += chunk_transcript + " "
        
        # Clean up the temporary chunk file
        os.remove(chunk_path)
    
    return transcript.strip()

# Transcribe each chunk by calling the external STT service
def transcribe_audio_chunk(audio_file: str, base_url: str) -> str:
    STT_API_ENDPOINT = base_url.rstrip('/') + '/start-brilla-ai'
    
    with open(audio_file, "rb") as f:
        audio_bytes = f.read()
        bytes_data = base64.b64encode(audio_bytes).decode()

        #TODO: request the actual round here
        payload = {"data": bytes_data, "filename": os.path.basename(audio_file), "current_round": current_round}
        response = requests.post(STT_API_ENDPOINT, json=payload)

        transcript = ""
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('transcript') is not None:
                transcript = response_data.get('transcript')

    return transcript

def send_audio_to_ML_layer(process_cmd: str, audio_chunks_dir_path: str, base_url: str):

    while True:
        line = process_cmd.stdout.readline()
        audio_line_match = re.search(r"\baudio\w+.wav", line)

        if audio_line_match:
            # wait for the audio to be written to file before sending 
            time.sleep(3.5)
            audio_chunk_file_name = audio_line_match.group()
            full_audio_path = os.path.join(audio_chunks_dir_path, audio_chunk_file_name)

            if os.path.isfile(full_audio_path):
                # send to ML layer
                ML_API_ENDPOINT = base_url.rstrip('/') + '/start-brilla-ai'
            
                with open(full_audio_path, "rb") as f:
                    audio_bytes = f.read()
                    bytes_data = base64.b64encode(audio_bytes).decode()

                    #TODO: request the actual round here
                    payload = {"data": bytes_data, "filename": os.path.basename(full_audio_path), "current_round": current_round}
                    response = requests.post(ML_API_ENDPOINT, json=payload)

                    if response.status_code == 200:
                        res_json = response.json()
                        task_id = res_json.get("task_id")
                        print("Started Processing with task id:", task_id)
                    else:
                        print(f"Something went wrong: {response.status_code}")
                
                # remove file aftr processing
                os.remove(full_audio_path)

def get_manifest_url_download_link(video_url):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        stream_info = ydl.extract_info(video_url, download=False)
        downloadLink = ''
        isLiveStream = False
        jsonDumpInfo = json.dumps(ydl.sanitize_info(stream_info))
        jsonLoadsResp = json.loads(jsonDumpInfo)
        if jsonLoadsResp['is_live']:
            downloadLink = jsonLoadsResp['url']
            isLiveStream = True
        else:
            downloadLink = video_url
        return downloadLink, isLiveStream

def cleanup_audio_files(directory_path):
    # Get list of files in the directory
    files = os.listdir(directory_path)

    # Remove each file
    for file in files:
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

def process_audio_from_video(video_url, audio_chunks_dir_path, base_url):

    downloadLink, isLiveStream = get_manifest_url_download_link(video_url)

    if isLiveStream:
        extractedAudioTitle = downloadLink
    else:
        # create an audio file to contain full extracted audio
        if os.path.isfile('output.wav'):
            os.remove('output.wav')
        
        # download full audio of the youtube video
        with yt_dlp.YoutubeDL({"quiet": True, 'extract_audio': True, 'format': 'bestaudio', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'wav'}], 'outtmpl': 'output.%(ext)s'}) as ydl:
            ydl.download(downloadLink)

        extractedAudioTitle = 'output.wav'

    # in live stream, call fmpeg to extract the audio from the manifest youtube url and break into 5s chunks
    # in non-live stream, call ffmpeg to break the full audio into 5s chunks
    runAudioExtractCmd = subprocess.Popen('ffmpeg -i {} -vn -f segment -segment_time 5 {}'
                                        .format(extractedAudioTitle, os.path.join(audio_chunks_dir_path, 'audio%03d.wav')), 
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, 
                                        universal_newlines=True, shell=True, text=True)
    
    send_audio_to_ML_layer(runAudioExtractCmd, audio_chunks_dir_path, base_url)
    
    runAudioExtractCmd.communicate()