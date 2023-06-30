import streamlit as st
from utility import DEMO_AUDIO_1_PATH, realTimeLocalSTT

st.set_page_config(page_title="Speech To Text Demo", page_icon="🎙️", layout="wide")

st.markdown("# Speech To Text Demo🎙️")
st.write(
    """
    This demo illustrates a real time transcription of the Speech To Text Model of the NSMQ AI. Steps:
    - Play the audio,
    - Click "Transcribe"
    - See the real time transcription
    
    Enjoy!
    """
)

st.divider()

# audio file
audio_file = open(DEMO_AUDIO_1_PATH, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format="audio/mp3")

# realtime transcription
if st.button('Transcribe'):
    # TODO: get actual transcription from API and display
    realTimeLocalSTT(DEMO_AUDIO_1_PATH)
