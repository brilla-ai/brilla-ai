import streamlit as st
from utility import set_stt_api, set_qa_api, set_tts_api, get_stt_api, get_qa_api, get_tts_api, NO_API_SET_FLAG

st.set_page_config(page_title="API Setup", page_icon="🎙️", layout="wide")

st.markdown("# API Setup 🛠️")
st.write(
    """
    Set up the API URLs for each Machine Learning task
    """
)

partialSuccessStatus = st.empty()
errorStatus = st.empty()

# populate the fields with existing values if present
sttAPIVal = st.text_input('Speech To Text API', get_stt_api() if get_stt_api() != NO_API_SET_FLAG else "")
qaAPIVal = st.text_input('Question Answering API', get_qa_api() if get_qa_api() != NO_API_SET_FLAG else "")
ttsAPIVal = st.text_input('Text To Speech API', get_tts_api() if get_tts_api() != NO_API_SET_FLAG else "")

errorDetected = False
errorMsg = ''
partialSuccessMsg = ''
if st.button('Submit'):
    if sttAPIVal:
        partialSuccessMsg += ' STT API set successfully.'
        set_stt_api(sttAPIVal)
    else:
        errorMsg += ' STT API not set.'
        errorDetected = True

    if qaAPIVal:
        partialSuccessMsg += ' QA API set successfully.'
        set_qa_api(qaAPIVal)
    else:
        errorMsg += ' QA API not set.'
        errorDetected = True

    if ttsAPIVal:
        partialSuccessMsg += ' TTS API set successfully.'
        set_tts_api(ttsAPIVal)
    else:
        errorMsg += ' TTS API not set.'
        errorDetected = True

    if not errorDetected:
        partialSuccessStatus.success("API URLs Setup Successfully")
    else:
        partialSuccessStatus.success(partialSuccessMsg)
        errorStatus.error(errorMsg, icon="⚠️")
