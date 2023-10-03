import streamlit as st
from utility import autoplay_live_video, create_embed_link_from_url, get_url_manifest, extract_audio_from_live_stream, set_live_video_url, get_live_video_url, NO_LIVE_VIDEO_URL_FLAG
from authentication import is_user_authorized

st.set_page_config(page_title="NSMQ AI Live Quiz", page_icon="✨", layout="wide")

st.markdown("# NSMQ AI Live Quiz ✨")
st.write(
    """
    See the NSMQ AI in action against a live quiz!
    """
)

st.divider()

# display the input field only for authenticated user
# option to login not displayed here as unauthenticated users should only see the live video and no input option
if is_user_authorized():
    getLiveVideoURL = st.text_input('Live Video Link')

    if st.button('Submit'):
        set_live_video_url(getLiveVideoURL)

liveVideoURL = get_live_video_url()
if liveVideoURL != NO_LIVE_VIDEO_URL_FLAG:
    vidCol, aiOpsCol = st.columns([2,2])

    with vidCol:
        embedLink = create_embed_link_from_url(liveVideoURL)
        autoplay_live_video(embedLink)

    with aiOpsCol:
        urlManifest = get_url_manifest(liveVideoURL)
        # TODO: sanitize output to prevent command injection
        extract_audio_from_live_stream(urlManifest)
