import streamlit as st
from utility import check_api_values, ai_operation, DEMO_AUDIO_5_PATH, DEMO_VIDEO_5_PATH

st.set_page_config(page_title="NSMQ AI 2nd Demo", page_icon="💡", layout="wide")

st.markdown("# NSMQ AI 2nd Demo💡")
st.write(
    """
    This demo illustrates a real time operation of all components of the NSMQ AI. Enjoy!
    """
)

check_api_values()

st.divider()

# display end to end flow
ai_operation(DEMO_VIDEO_5_PATH, DEMO_AUDIO_5_PATH)
