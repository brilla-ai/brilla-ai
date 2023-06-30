import streamlit as st
from utility import aiOperation, DEMO_AUDIO_2_PATH, DEMO_VIDEO_2_PATH

st.set_page_config(page_title="NSMQ AI 2nd Demo", page_icon="💡", layout="wide")

st.markdown("# NSMQ AI 2nd Demo💡")
st.write(
    """
    This demo illustrates a real time operation of all components of the NSMQ AI. Enjoy!
    """
)

st.divider()

# display end to end flow
aiOperation(DEMO_VIDEO_2_PATH, DEMO_AUDIO_2_PATH)
