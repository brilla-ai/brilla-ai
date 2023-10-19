import streamlit as st
import requests
from pydub import AudioSegment
import os
import tempfile
from streamlit_webrtc import WebRtcMode, webrtc_streamer
import queue
import base64
import json
import uuid
import time
import os 
import yt_dlp
import subprocess
import re
from urllib.parse import urlparse, parse_qs, urljoin
from authentication import is_prod_mode


CURRENT_DIR =  os.getcwd()
VIDEO_DIR = os.path.join(CURRENT_DIR, 'streamlitDemo/assets/video/' if is_prod_mode() else 'assets/video/')
AUDIO_DIR = os.path.join(CURRENT_DIR, 'streamlitDemo/assets/audio/' if is_prod_mode() else 'assets/audio/')

# VIDEO PATHS
DEMO_VIDEO_1_PATH  = VIDEO_DIR  + 'video1.mp4'
DEMO_VIDEO_2_PATH  = VIDEO_DIR  + 'video2.mp4'
DEMO_VIDEO_3_PATH  = VIDEO_DIR  + 'video3.mp4'
DEMO_VIDEO_4_PATH  = VIDEO_DIR  + 'video4.mp4'
DEMO_VIDEO_5_PATH  = VIDEO_DIR  + 'video5.mp4'

# AUDIO PATHS
DEMO_AUDIO_1_PATH  = AUDIO_DIR + 'audio_video1.mp3'
DEMO_AUDIO_2_PATH  = AUDIO_DIR + 'audio_video2.mp3'
DEMO_AUDIO_3_PATH  = AUDIO_DIR + 'audio_video3.mp3'
DEMO_AUDIO_4_PATH  = AUDIO_DIR + 'audio_video4.mp3'
DEMO_AUDIO_5_PATH  = AUDIO_DIR + 'audio_video5.mp3'

# API ENDPOINTS
STT_API_KEY = 'STT_API'
QA_API_KEY = 'QA_API'
TTS_API_KEY = 'TTS_API'
ALL_IN_ONE_API_KEY = 'ALL_IN_ONE_API'
NO_API_SET_FLAG = '-1'

# API SETUP PAGE
INDIVIDUAL_API_SETUP = 'INV_APIS'
ALL_IN_ONE_API_SETUP = 'ALL_API'

# LIVE MODE FLAGS
LIVE_VIDEO_URL_KEY = 'LIVE_VIDEO_URL'
NO_LIVE_VIDEO_URL_FLAG = '-1'

# QA RIDDLE VALUES
QA_QUESTION_BANK = {
    "riddle1": "there is really nothing improper about me,i am just a fraction,my numerator exceeds my denominator,i am not a mixed fraction or mixed number,an example of me is 7 3",
    "riddle2": "i am a metallic element, i belong to one of the major series in the periodic table characterised by incomplete 5 f subshell	, i was named after a planet in the solar system, i show variable valences of 2345 and 6, i have several isotopes whose masses spread over a range of 15 mass units but all having atomic number of 92, i nuclear weapons and nuclear energy generation we are all synonymous",
    "riddle3": "i am used metaphorically to refer to reasoning or decision making that is narrow in scope	in science, i am a common condition that affects many people in the world, my underlying cause is believed to be a combination of genetic and environmental factors, i occur if the eyeball is too long or the cornea is too curved are you extremely myopic, i am the condition in which one unable to see distant objects clearly because the images are focused in front of the retina of the eye"
    }

# TTS VOICE OPTIONS
TTS_VOICE_BANK = {
    "voice1": "Ghanaian (Voice 1)",
    "voice2": "Ghanaian (Voice 2)"
}

# DEFAULTS FOR REAL TIME AUDIO RECORDING TRANSCRIPTION
TIMEOUT = 3  # Timeout for getting frames from the audio receiver. Default is 3 seconds.

# API FUNCTIONS
def get_stt_transcript(audioFile):
    STT_API = get_stt_api()

    # only make the API call if a valid url is present
    if STT_API != NO_API_SET_FLAG:
        STT_TRANSCRIPT_API = STT_API.rstrip('/') + '/get-transcript'
        with open(audioFile, "rb") as audio_file:
            audio_bytes = audio_file.read()
            bytes_data = base64.b64encode(audio_bytes).decode()

            # Create payload
            payload = {"data": bytes_data, "filename": "temp_audio.wav"}
            payload = json.dumps(payload)

            # Send GET request to API endpoint
            response = requests.get(STT_TRANSCRIPT_API, data=payload)

            if response.status_code == 200:
                transcript = response.json()['transcript']
                clues = response.json()['clues']
                clue_count = response.json()['clue_count']
                is_start_of_riddle = response.json()['is_start_of_riddle']
                is_end_of_riddle = response.json()['is_end_of_riddle']
                print('transcript:',transcript)
                print('clues:',clues)
                print('clue_count:',clue_count)
                print('is_start_of_riddle:',is_start_of_riddle)
                print('is_end_of_riddle:',is_end_of_riddle)

                return transcript, clues, clue_count, is_start_of_riddle, is_end_of_riddle

def get_qa_answer(question, mode="demo", clues="", clue_count=0, is_start_of_riddle=False, is_end_of_riddle=False):
    QA_API = get_qa_api()

    # only make the API call if a valid url is present
    if QA_API != NO_API_SET_FLAG:
        if mode == "demo":
            question = json.dumps({'text' : question})
            response = requests.get(QA_API.rstrip('/') + '/demo_qa', data=question)
        elif mode == "live":
            payload = json.dumps({'clues' : clues, 'clue_count' : clue_count, 'is_start_of_riddle' : is_start_of_riddle, 'is_end_of_riddle' : is_end_of_riddle})
            response = requests.get(QA_API.rstrip('/') + '/live_qa', data=payload)

        if response.status_code == 200:
            falconAnswer = response.json()['falcon']
            chatGPTAnswer = ""
            if mode == "live":
                chatGPTAnswer = response.json()['chatGPT']
            return falconAnswer, chatGPTAnswer

def get_tts_audio(text, voice, mode="demo"):
    TTS_API = get_tts_api()
    # only make the API call if a valid url is present
    if TTS_API != NO_API_SET_FLAG:
        voiceOption = '1' if voice == TTS_VOICE_BANK['voice1'] else '2'

        payload = json.dumps({'text' : text, 'voice': voiceOption})
        if mode == "demo":
            response = requests.get(TTS_API.rstrip('/') + '/demo_tts', data=payload)
        elif mode == "live":
            response = requests.get(TTS_API.rstrip('/') + '/live_tts', data=payload)

        outputFileName = "tts_output.wav"

        if response.status_code == 200:
            with open(outputFileName, "wb+") as file:
                file.write(response.content)
    
    return outputFileName

# SET API IN ENVIRONMENT VARIABLES
def set_stt_api(apiVal):
    os.environ[STT_API_KEY] = apiVal

def set_qa_api(apiVal):
    os.environ[QA_API_KEY] = apiVal

def set_tts_api(apiVal):
    os.environ[TTS_API_KEY] = apiVal

def set_all_in_one_api(apiVal):
    os.environ[ALL_IN_ONE_API_KEY] = apiVal

    # also set each indiviudal api
    set_stt_api(apiVal)
    set_qa_api(apiVal)
    set_tts_api(apiVal)

# GET API IN ENVIRONMENT VARIABLES
def get_stt_api():
    return os.environ.get(STT_API_KEY, NO_API_SET_FLAG)

def get_qa_api():
    return os.environ.get(QA_API_KEY, NO_API_SET_FLAG)
    
def get_tts_api():
    return os.environ.get(TTS_API_KEY, NO_API_SET_FLAG)

def get_all_in_one_api():
    return os.environ.get(ALL_IN_ONE_API_KEY, NO_API_SET_FLAG)

# FUNCTIONS TO TEST APIs
def is_api_valid(apiURL, apiKey):
    testEndpoint = ''

    # if url is empty return false
    if apiURL == '':
        return False

    if apiKey == STT_API_KEY:
        testEndpoint = '/stt-test'
    elif apiKey == QA_API_KEY:
        testEndpoint = '/qa-test'
    elif apiKey == TTS_API_KEY:
        testEndpoint = '/tts-test'
    else:
        return False

    # perform endpoint test
    TEST_API = apiURL.rstrip('/') + testEndpoint
    response = requests.get(TEST_API)

    if response.status_code == 200:
        return True

def is_stt_api_valid(apiURL):
    return is_api_valid(apiURL, STT_API_KEY)

def is_qa_api_valid(apiURL):
    return is_api_valid(apiURL, QA_API_KEY)

def is_tts_api_valid(apiURL):
    return is_api_valid(apiURL, TTS_API_KEY)

def is_all_in_one_api_valid(apiURL):
    return is_stt_api_valid(apiURL) and is_qa_api_valid(apiURL) and is_tts_api_valid(apiURL)

def apiSetupPageOperation(inputType):
    successStatus = st.empty()
    errorStatus = st.empty()

    errorDetected = False
    errorMsg = ''
    partialSuccessMsg = ''

    sttAPIVal = ''
    qaAPIVal = ''
    ttsAPIVal = ''
    allInOneAPIVal = ''
    keyVal = ''

    # flags to determine if APIs should be set
    setSTTAPI = False
    setQAAPI = False
    setTTSAPI = False
    setALLAPI = False

    # display section based on page
    if inputType == INDIVIDUAL_API_SETUP:
        keyVal = 'individual-url'
        sttAPIVal = st.text_input('Speech To Text API', get_stt_api() if get_stt_api() != NO_API_SET_FLAG else "")
        qaAPIVal = st.text_input('Question Answering API', get_qa_api() if get_qa_api() != NO_API_SET_FLAG else "")
        ttsAPIVal = st.text_input('Text To Speech API', get_tts_api() if get_tts_api() != NO_API_SET_FLAG else "")
    elif inputType == ALL_IN_ONE_API_SETUP:
        keyVal = 'all-in-one-url'
        allInOneAPIVal = st.text_input('All In One API', get_all_in_one_api() if get_all_in_one_api() != NO_API_SET_FLAG else "")
        sttAPIVal = allInOneAPIVal
        qaAPIVal = allInOneAPIVal
        ttsAPIVal = allInOneAPIVal

    if st.button('Submit', key=keyVal):
        with st.spinner('Validating APIs'):
            # validate APIs
            if is_stt_api_valid(sttAPIVal):
                partialSuccessMsg += ' STT API endpoint set successfully.'
                setSTTAPI = True
            else:
                errorMsg += ' STT API endpoint is not active.'
                errorDetected = True

            if is_qa_api_valid(qaAPIVal):
                partialSuccessMsg += ' QA API endpoint set successfully.'
                setQAAPI = True
            else:
                errorMsg += ' QA API endpoint is not active.'
                errorDetected = True

            if is_tts_api_valid(ttsAPIVal):
                partialSuccessMsg += ' TTS API endpoint set successfully.'
                setTTSAPI = True
            else:
                errorMsg += ' TTS API endpoint is not active.'
                errorDetected = True
            
            if is_all_in_one_api_valid(allInOneAPIVal):
                setALLAPI = True

            # set APIs
            if inputType == INDIVIDUAL_API_SETUP:
                if setSTTAPI:
                    set_stt_api(sttAPIVal)
                if setTTSAPI:
                    set_tts_api(ttsAPIVal)
                if setQAAPI:
                    set_qa_api(qaAPIVal)
            elif inputType == ALL_IN_ONE_API_SETUP:
                if setALLAPI:
                    set_all_in_one_api(allInOneAPIVal)

            if not errorDetected:
                successStatus.success("All API endpoints set successfully.")
            else:
                if partialSuccessMsg:
                    successStatus.success(partialSuccessMsg)
                errorStatus.error(errorMsg, icon="⚠️")

# AUTOPLAY AUDIO
def autoplay_audio(audioFile):
    with open(audioFile, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <audio controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
            </audio>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

# AUTOPLAY VIDEO
def autoplay_video(video_file_path):
    with open(video_file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        md = f"""
            <video width="550" height="400" controls autoplay="true">
            <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            </video>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )

def autoplay_live_video(video_url):
    md = f"""
        <iframe width="550" height="400" src="{video_url}?autoplay=1&mute=1">
        </iframe>
        """
    
    st.markdown(
        md,
        unsafe_allow_html=True,
    )


# STT PROCESSING
def realtime_audio_file_STT(audio_file_path, labelFlag="hidden"):
    with st.spinner('Transcribing'):
        # creating a placeholder for the fixed sized textbox
        transcriptBox = st.empty()
        transcriptText = ''
        boxHeight = 200
        transcriptBox.text_area(
            "Question",
            transcriptText,
            key=uuid.uuid4(),
            label_visibility = labelFlag,
            height = boxHeight
        )

        # temp location for audio chunks
        temp_dir = tempfile.mkdtemp()
        audio_chunk_temp_file = os.path.join(temp_dir, "temp.wav")

        # majority of audio chunk code referenced from https://www.geeksforgeeks.org/audio-processing-using-pydub-and-google-speechrecognition-api/#
        
        # Input audio file to be sliced
        audio = AudioSegment.from_mp3(audio_file_path)

        # Length of the audiofile in milliseconds
        n = len(audio)

        # Interval length at which to slice the audio file.
        # If length is 22 seconds, and interval is 5 seconds,
        # The chunks created will be:
        # chunk1 : 0 - 5 seconds
        # chunk2 : 5 - 10 seconds
        # chunk3 : 10 - 15 seconds
        # chunk4 : 15 - 20 seconds
        # chunk5 : 20 - 22 seconds
        # 5seconds proved to be the best interval to make the transcription correspond to the audio which is autoplayed in the UI
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
            sound_chunk = audio[start:end]

            # Store the sliced audio file
            sound_chunk.export(audio_chunk_temp_file, format ="wav")
            
            # Slicing of the audio file is done. transcribe audio chunks
            time.sleep(2)
            transcriptText += get_stt_transcript(audio_chunk_temp_file)[0]
            os.remove(audio_chunk_temp_file)

            transcriptBox.text_area("Question", transcriptText, key=uuid.uuid4(), label_visibility=labelFlag, height = boxHeight)

            # Check for flag.
            # If flag is 1, end of the whole audio reached.
            if flag == 1:
                break

    return transcriptText

def realtime_audio_recording_STT():
    # temp location for audio chunks
    temp_dir = tempfile.mkdtemp()
    audio_chunk_temp_file = os.path.join(temp_dir, "recording_temp.wav")

    # streamlit-webrtc component containing the audio functionality
    webrtc_ctx = webrtc_streamer(
        key="speech-to-text",
        mode=WebRtcMode.SENDONLY,
        audio_receiver_size=1024,
        media_stream_constraints={"video": False, "audio": True},
    )

    # creating a placeholder for the fixed sized textbox
    with st.spinner("Running..Say Something!"):
        transcriptBox = st.empty()
        transcriptText = ''
        transcriptBox.text_area(
            "Real time transcription",
            transcriptText,
            label_visibility  = 'hidden',
            key=uuid.uuid4()
        )
    
        while webrtc_ctx.state.playing:
            if webrtc_ctx.audio_receiver:
                try:
                    audio_frames = webrtc_ctx.audio_receiver.get_frames(timeout=TIMEOUT)
                except queue.Empty:
                    continue

                sound_chunk = AudioSegment.empty()
                for audio_frame in audio_frames:
                    sound = AudioSegment(
                        data=audio_frame.to_ndarray().tobytes(),
                        sample_width=audio_frame.format.bytes,
                        frame_rate=audio_frame.sample_rate,
                        channels=len(audio_frame.layout.channels),
                    )
                    sound_chunk += sound
                
                if len(sound_chunk) > 0:
                    sound_chunk.export(audio_chunk_temp_file, format ="wav")
                    transcriptText += get_stt_transcript(audio_chunk_temp_file)[0]
                    transcriptBox.text_area("", transcriptText)
                    os.remove(audio_chunk_temp_file)
            else:
                break

# QA PROCESSING
def realtime_question_answering(riddle, labelFlag="hidden", mode="demo", clues="", clue_count=0, is_start_of_riddle=False, is_end_of_riddle=False):
    answerBoxText = ''

    with st.spinner("Working On Answer!"):
        answerBox = st.empty()
        answerBox.text_area("Answer", answerBoxText, height = 10, label_visibility=labelFlag, key=uuid.uuid4())
        if mode == "demo":
            falconAnswer = get_qa_answer(riddle)[0]
        elif mode == "live":
            falconAnswer, chatGPTAnswer = get_qa_answer(riddle, mode, clues, clue_count, is_start_of_riddle, is_end_of_riddle)
        answerBoxText = falconAnswer
    
    answerBox.text_area("Answer", answerBoxText, key=uuid.uuid4())
    if mode == "live" and len(chatGPTAnswer.strip()) != 0:
        st.markdown("**:green[ChatGPT's Answer]**: " + "*:green[" + chatGPTAnswer + "]*")

    return answerBoxText

# TTS PROCESSING
def realtime_text_to_speech(text, voice, mode="demo"):
    outputAudioFile = ''
    with st.spinner('Generating speech...'):
        outputAudioFile = get_tts_audio(text, voice, mode)
    autoplay_audio(outputAudioFile)

# OVERALL END TO END OPERATION DISPLAY
def ai_in_demo_mode(video_file_path, audio_file_path):
    if not check_api_values():
        return

    videoCol, aiResponseCol = st.columns([3,2])

    with videoCol:
        autoplay_video(video_file_path)

    with aiResponseCol:
        transcript = realtime_audio_file_STT(audio_file_path, "visible")
        answer = realtime_question_answering(transcript, "visible")

        st.text('Generated Speech')
        realtime_text_to_speech(answer, TTS_VOICE_BANK['voice2'])

def check_api_values():
    isValid = True
    if get_stt_api() == NO_API_SET_FLAG:
        isValid = False
        st.warning('Please setup the STT API endpoint on the API Setup page', icon="⚠️")
    
    if get_tts_api() == NO_API_SET_FLAG:
        isValid = False
        st.warning('Please setup the TTS API endpoint on the API Setup page', icon="⚠️")

    if get_qa_api() == NO_API_SET_FLAG:
        isValid = False
        st.warning('Please setup the QA API endpoint on the API Setup page', icon="⚠️")
    
    return isValid

# LIVE VIDEO AUDIO EXTRACTION OPERATIONS
def set_live_video_url(liveVideoUrl):
    os.environ[LIVE_VIDEO_URL_KEY] = liveVideoUrl

def get_live_video_url():
    return os.environ.get(LIVE_VIDEO_URL_KEY, NO_LIVE_VIDEO_URL_FLAG)

def create_embed_link_from_url(liveVideoURL):
        urlData = urlparse(liveVideoURL)
        query = parse_qs(urlData.query)

        # convert youtube link to an embed link
        return urljoin("https://www.youtube.com/embed/", query["v"][0])

def get_url_download_link(liveVideoURL):
    with yt_dlp.YoutubeDL({"quiet": True}) as ydl:
        streamInfo = ydl.extract_info(liveVideoURL, download=False)
        downloadLink = ''
        isLiveStream = False
        jsonDumpInfo = json.dumps(ydl.sanitize_info(streamInfo))
        jsonLoadsResp = json.loads(jsonDumpInfo)
        if jsonLoadsResp['is_live']:
            downloadLink = jsonLoadsResp['url']
            isLiveStream = True
        else:
            downloadLink = liveVideoURL
        return downloadLink, isLiveStream
    
def ai_in_live_mode(tempDir, processCmd):
    with st.spinner('Transcribing'):
        # creating a placeholder for the fixed sized textbox
        transcriptText = ''
        boxHeight = 200
        label_flag = "visible"
        transcriptBox = st.empty()

        transcriptBox.text_area(
                "Question",
                transcriptText,
                key=uuid.uuid4(),
                label_visibility = label_flag,
                height = boxHeight
            )

        riddleAnswered = False
        while True:
            line = processCmd.stdout.readline()
            audioLineMatch = re.search(r"\baudio\w+.mp3", line)

            if audioLineMatch:
                # wait for the audio to be written to file before sending 
                time.sleep(2)
                audioChunkFileName = audioLineMatch.group()
                fullAudioPath = os.path.join(tempDir, audioChunkFileName)

                if os.path.isfile(fullAudioPath):
                    transcript, clues, clue_count, is_start_of_riddle, is_end_of_riddle = get_stt_transcript(fullAudioPath)
                    transcriptText += transcript
                
                transcriptBox.text_area("Question", transcriptText, key=uuid.uuid4(), label_visibility=label_flag, height = boxHeight)

                if is_start_of_riddle == True:
                    riddleAnswered = False

                # only send to QA if STT provided clues
                answer = ''
                # send question to QA if clue is present and riddle has not been answered
                if len(clues.strip()) != 0 and not riddleAnswered:
                    answer = realtime_question_answering(transcript, "visible", "live", clues, clue_count, is_start_of_riddle, is_end_of_riddle)

                if len(answer.strip()) != 0:
                    # mark riddle as answered
                    riddleAnswered = True
                    st.text('Generated Speech')
                    realtime_text_to_speech(answer, TTS_VOICE_BANK['voice2'], "live")

def process_youtube_video(downloadLink, isLiveStream):
    if isLiveStream:
        extractedAudioTitle = downloadLink
    else:
        # create an audio file to contain full extracted audio
        extractedAudioTitle = 'output.opus'
        # download full audio of the youtube video
        with yt_dlp.YoutubeDL({"quiet": True, 'extract_audio': True, 'format': 'bestaudio', 'outtmpl': extractedAudioTitle}) as ydl:
            ydl.download(downloadLink)

    # in both live stream and non live stream cases, use ffmpeg to convert the extracted audio to mp3 and split into 5s chunks
    tempDir = tempfile.mkdtemp()
    runAudioExtractCmd = subprocess.Popen('ffmpeg -i {} -vn -acodec libmp3lame -f segment -segment_time 5 {}'
                                        .format(extractedAudioTitle, os.path.join(tempDir, "audio%03d.mp3")), 
                                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT, bufsize=1, 
                                        universal_newlines=True, shell=True)
    ai_in_live_mode(tempDir, runAudioExtractCmd)

    # cleanup created audio file if we are not in live stream
    if not isLiveStream:
        os.remove(extractedAudioTitle)
    
    runAudioExtractCmd.communicate()
