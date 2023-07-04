import streamlit as st
from utility import ai_operation, DEMO_AUDIO_3_PATH, DEMO_VIDEO_3_PATH

st.set_page_config(page_title="NSMQ AI 3rd Demo", page_icon="💡", layout="wide")

st.markdown("# NSMQ AI 2nd Demo💡")
st.write(
    """
    This demo illustrates a real time operation of all components of the NSMQ AI. Enjoy!
    """
)

st.divider()

# display end to end flow
ai_operation(DEMO_VIDEO_3_PATH, DEMO_AUDIO_3_PATH)
