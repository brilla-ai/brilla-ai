import streamlit as st
from utility import get_tts_api, realtime_text_to_speech, TTS_VOICE_BANK, NO_API_SET_FLAG

st.set_page_config(page_title="Text To Speech", page_icon="🔉", layout="wide")

st.markdown("# Text To Speech Demo🔉")
st.write(
    """
    This demo illustrates a real time operation of the Text To Speech Model of the NSMQ AI.
    """
)

if get_tts_api() == NO_API_SET_FLAG:
    st.warning('Please setup the TTS API endpoint on the API Setup page', icon="⚠️")

st.divider()

# placeholder for error message
errorMsg = st.empty()

# choose voice options
voice = st.radio('Select A Voice', (TTS_VOICE_BANK['voice1'], TTS_VOICE_BANK['voice2']), horizontal=True)

# text input-dropdown

text= st.selectbox(
'Select Text',
(
"I am the set of all possible positions a point can take. I may be a region in a plane or in space, but more often I am a continuous curve.Who am I?",
"One particular element out of about the hundred or so elements in the Periodic Table is always present during my operations. I am the secret behind the relatively high boiling point of water. Who am i?",
"Welcome to the national science and maths quiz.", "I am not one who likes much talk. I prefer action, so I'm on the side of forces. I am available when you need to turn things around and rotate objects about a point. Who am I?"
    
)
)

st.write('You selected:', text )


# generated audio file
if st.button('Get Generated Speech!'):
    # check that text box has a value
    if text:
        realtime_text_to_speech(text, voice)
    else:
        errorMsg.error('Please provide a text', icon="⚠️")
