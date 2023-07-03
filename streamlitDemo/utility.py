import streamlit as st
import requests
from pydub import AudioSegment
import whisper
import os
import glob
from pathlib import Path

# VIDEO PATHS
DEMO_VIDEO_1_PATH = './assets/video/video1.mp4'
DEMO_VIDEO_2_PATH  = './assets/video/video2.mp4'
DEMO_VIDEO_3_PATH  = './assets/video/video3.mp4'

# AUDIO PATHS
DEMO_AUDIO_1_PATH  = './assets/audio/audio_video1.mp3'
DEMO_AUDIO_2_PATH  = './assets/audio/audio_video2.mp3'
DEMO_AUDIO_3_PATH  = './assets/audio/audio_video3.mp3'

# AUDIO CHUNK FOLDER
AUDIO_CHUNK_FOLDER_PATH = './audioChunks'

# API ENDPOINTS
STT_API = ''
QA_API = ''
TTS_API = ''

# TEST VALUES
DEMO_QA_QUESTION = {"text": "there is really nothing improper about me,i am just a fraction,my numerator exceeds my denominator,i am not a mixed fraction or mixed number,an example of me is 7 3"}
DEMO_QA_ANSWER = {"answer": "improper fraction"}

# API FUNCTIONS
def get_stt_text():
    response = requests.get(STT_API)
    return response.json()

def get_qa_answer(question):
    response = requests.get(QA_API, data=question)
    return response.json()['answer']

def get_tts_audio(answer):
    response = requests.get(TTS_API, data=answer)
    #TODO: change from json to audio
    return response.json()

# LOCAL STT PROCESSING
def realTimeLocalSTT(audio_file_path):
    # clean up audio chunk folder in case there is anything in there
    cleanupAudioChunkFiles()

    # creating a placeholder for the fixed sized textbox
    transcriptBox = st.empty()
    transcriptText = ''
    boxHeight = 180
    transcriptBox.text_area(
        "Real time transcription",
        transcriptText,
        height = boxHeight,
        label_visibility  = 'hidden'
    )

    # setup whisper models
    whisperModel = whisper.load_model("base")

    # majority of audio chunk code referenced from https://www.geeksforgeeks.org/audio-processing-using-pydub-and-google-speechrecognition-api/#
    
    # Input audio file to be sliced
    audio = AudioSegment.from_mp3(audio_file_path)

    # Length of the audiofile in milliseconds
    n = len(audio)

    # Variable to count the number of sliced chunks
    counter = 1

    # Interval length at which to slice the audio file.
    # If length is 22 seconds, and interval is 5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 5 - 10 seconds
    # chunk3 : 10 - 15 seconds
    # chunk4 : 15 - 20 seconds
    # chunk5 : 20 - 22 seconds
    interval = 5 * 1000

    # Length of audio to overlap.
    # If length is 22 seconds, and interval is 5 seconds,
    # With overlap as 1.5 seconds,
    # The chunks created will be:
    # chunk1 : 0 - 5 seconds
    # chunk2 : 3.5 - 8.5 seconds
    # chunk3 : 7 - 12 seconds
    # chunk4 : 10.5 - 15.5 seconds
    # chunk5 : 14 - 19.5 seconds
    # chunk6 : 18 - 22 seconds
    overlap = 0

    # Initialize start and end seconds to 0
    start = 0
    end = 0
    
    # Flag to keep track of end of file.
    # When audio reaches its end, flag is set to 1 and we break
    flag = 0

    # Iterate from 0 to end of the file,
    # with increment = interval
    for i in range(0, 2 * n, interval):
        
        # During first iteration,
        # start is 0, end is the interval
        if i == 0:
            start = 0
            end = interval
    
        # All other iterations,
        # start is the previous end - overlap
        # end becomes end + interval
        else:
            start = end - overlap
            end = start + interval
    
        # When end becomes greater than the file length,
        # end is set to the file length
        # flag is set to 1 to indicate break.
        if end >= n:
            end = n
            flag = 1
    
        # Storing audio file from the defined start to end
        chunk = audio[start:end]
    
        # Filename / Path to store the sliced audio
        # extracting just the name of the file out of the path
        filename = AUDIO_CHUNK_FOLDER_PATH + './' + os.path.splitext(os.path.basename(audio_file_path))[0] + '_chunk' + str(counter) + '.mp3'
    
        # Store the sliced audio file to the defined path
        chunk.export(filename, format ="mp3")
    
        # Increment counter for the next chunk
        counter = counter + 1
        
        # Slicing of the audio file is done.

        # transcribe model
        transcription = whisperModel.transcribe(filename)
        transcriptText += transcription['text']
        transcriptBox.text_area("", transcriptText, height = boxHeight)

        # Check for flag.
        # If flag is 1, end of the whole audio reached.
        # Close the file and break.
        if flag == 1:
            break

    # clean up audio chunk folder since processing is complete
    cleanupAudioChunkFiles()

# CLEAN UP OF AUDIO CHUNK FILES
def cleanupAudioChunkFiles():
    for f in Path(AUDIO_CHUNK_FOLDER_PATH).glob('*.mp3'):
        try:
            f.unlink()
        except OSError as e:
            print("Error: %s : %s" % (f, e.strerror))

# OVERALL END TO END OPERATION DISPLAY
def aiOperation(video_file_path, audio_file_path):
    videoCol, rttCol = st.columns([3,2])

    with videoCol:
        vid1_file = open(video_file_path, 'rb')
        vid1_bytes = vid1_file.read()
        st.video(vid1_bytes)

    with rttCol:
        if st.button('Transcribe'):
            realTimeLocalSTT(audio_file_path)

    st.divider()

    questionCol, answerCol = st.columns([1.5,1])

    with questionCol:
        st.write("#### Question")
        # st.write(QA_QUESTION["text"])
        # st.write(get_stt_text()['reference'])
        st.text_area("Question", DEMO_QA_QUESTION["text"], label_visibility  = 'hidden')
        
    with answerCol:
        st.write("#### Answer")
        # st.write(QA_ANSWER["answer"])
        # st.write(get_qa_answer(question))
        st.text_area("Answer", DEMO_QA_ANSWER["answer"], label_visibility  = 'hidden')
    
    st.divider()

    st.write('#### Generated Speech')

    # TODO: get actual audio from API and display
    audio_file = open(audio_file_path, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

