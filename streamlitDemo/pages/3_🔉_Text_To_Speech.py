import streamlit as st
from utility import DEMO_QA_ANSWER, DEMO_AUDIO_1_PATH, get_tts_audio

st.set_page_config(page_title="Text To Speech", page_icon="🔉", layout="wide")

st.markdown("# Text To Speech Demo🔉")
st.write(
    """
    This demo illustrates a real time operation of the Text To Speech Model of the NSMQ AI. Steps:
    - Enter Text
    - Click "Get Generated Speech!"
    - Play the real time generated audio
    
    Enjoy!
    """
)

st.divider()

# text input
answer = st.text_area("Enter Text", DEMO_QA_ANSWER['answer'], placeholder = DEMO_QA_ANSWER['answer'], height = 80)

# generated audio file
if st.button('Get Generated Speech!'):
    # TODO: get actual audio from API and display
    #st.write(get_tts_audio(answer))
    audio_file = open(DEMO_AUDIO_1_PATH, 'rb')
    audio_bytes = audio_file.read()
    st.audio(audio_bytes, format="audio/mp3")
