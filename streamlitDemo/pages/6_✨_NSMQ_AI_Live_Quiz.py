import streamlit as st
from utility import get_url_manifest, extract_audio_from_live_stream

st.set_page_config(page_title="NSMQ AI Live Quiz", page_icon="✨", layout="wide")

st.markdown("# NSMQ AI Live Quiz ✨")
st.write(
    """
    See the NSMQ AI in action against a live quiz!
    """
)

st.divider()

liveVideoURL = st.text_input('Live Video Link')

if st.button('Submit'):
    vidCol, aiOpsCol = st.columns([2,2])

    with vidCol:
        st.video(liveVideoURL, start_time=0)

    with aiOpsCol:
        urlManifest = get_url_manifest(liveVideoURL)
        with st.spinner('Transcribing'):
            extract_audio_from_live_stream(urlManifest)
