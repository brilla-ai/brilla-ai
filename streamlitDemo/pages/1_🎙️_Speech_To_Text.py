import streamlit as st
from utility import DEMO_AUDIO_3_PATH, realTimeAudioFileSTT, realTimeAudioRecordingSTT

st.set_page_config(page_title="Speech To Text Demo", page_icon="🎙️", layout="wide")

st.markdown("# Speech To Text Demo🎙️")
st.write(
    """
    This demo illustrates a real time transcription of the Speech To Text Model of the NSMQ AI. 
    Try out an audio sample or test with a live recording of your own voice!
    """
)

sampleAudioTab, testUserAudioTab = st.tabs(["AUDIO SAMPLE", "TEST LIVE RECORDING"])

with sampleAudioTab:
    st.write(
        """
        This demo illustrates a real time transcription of the Speech To Text Model of the NSMQ AI. Steps:
        - Play the audio
        - Click "Transcribe"
        - See the real time transcription
        
        Enjoy!
        """
    )

    # audio file
    audio_file = open(DEMO_AUDIO_3_PATH, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")

    # realtime transcription
    if st.button('Transcribe'):
        # TODO: get actual transcription from API and display
        realTimeAudioFileSTT(DEMO_AUDIO_3_PATH)


with testUserAudioTab:
    st.write(
        """
        Steps:
        - Click "Start Recording"
        - Say something
        - See the real time transcription   
        - Click "Stop Recording" 
        """
    )

    # session for controlling the start/stop button
    if 'record' not in st.session_state:
        st.session_state.record = False

    def clickStartButton():
        st.session_state.record = True
    
    def clickStopButton():
        st.session_state.record = False

    startCol, stopCol = st.columns(2)

    with startCol:
        st.button('Start Recording', on_click=clickStartButton)
    
    with stopCol:
        st.button('Stop Recording', on_click=clickStopButton)

    if st.session_state.record:
        with st.spinner('Transcribing Your Voice...Say Something'):
            realTimeAudioRecordingSTT()

