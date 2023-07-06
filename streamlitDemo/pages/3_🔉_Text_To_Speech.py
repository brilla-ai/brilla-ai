import streamlit as st
from utility import get_tts_api, realtime_text_to_speech, TTS_VOICE_BANK

st.set_page_config(page_title="Text To Speech", page_icon="🔉", layout="wide")

st.markdown("# Text To Speech Demo🔉")
st.write(
    """
    This demo illustrates a real time operation of the Text To Speech Model of the NSMQ AI.
    """
)

if get_tts_api() == '-1':
    st.warning('Please setup the TTS API on the API Setup page', icon="⚠️")

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
        realtime_text_to_speech(text, voice)
    else:
        errorMsg.error('Please provide a text', icon="⚠️")
