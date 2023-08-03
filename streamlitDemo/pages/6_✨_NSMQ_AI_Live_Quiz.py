import streamlit as st
from utility import ai_operation, DEMO_AUDIO_5_PATH, DEMO_VIDEO_5_PATH

st.set_page_config(page_title="NSMQ AI Live Quiz", page_icon="✨", layout="wide")

st.markdown("# NSMQ AI Live Quiz ✨")
st.write(
    """
    Select a live video option to see the NSMQ AI in action against a live quiz!
    """
)

st.divider()

# utilizing 5 in order to align the 2nd column closer to the 1st
nsmqGhanaCol, joyPrimeCol = st.columns([1,5])

liveVideoVal = ''

with nsmqGhanaCol:
    if st.button('NSMQ GHANA'):
        liveVideoVal = 'https://www.youtube.com/embed/mNR8aHWE3Mc'

with joyPrimeCol:
    if st.button('JOY PRIME'):
        liveVideoVal = 'https://www.youtube.com/embed/PG2HPAPkaaw'

st.components.v1.iframe(liveVideoVal, width=550, height=400)
