import streamlit as st
from utility import get_tts_audio, autoplay_audio, TTS_VOICE_BANK

st.set_page_config(page_title="Text To Speech", page_icon="🔉", layout="wide")

st.markdown("# Text To Speech Demo🔉")
st.write(
    """
    This demo illustrates a real time operation of the Text To Speech Model of the NSMQ AI.
    """
)

st.divider()

# placeholder for error message
errorMsg = st.empty()

# choose voice options
voice = st.radio('Select A Voice', (TTS_VOICE_BANK['voice1'], TTS_VOICE_BANK['voice2']), horizontal=True)

# text input
text = st.text_area("Enter Text", '', height = 80)

# generated audio file
if st.button('Get Generated Speech!'):
    # check that text box has a value
    if text:
        outputAudioFile = ''
        with st.spinner('Generating speech...'):
            outputAudioFile = get_tts_audio(text, voice)
        autoplay_audio(outputAudioFile)
    else:
        errorMsg.error('Please provide a text', icon="⚠️")
