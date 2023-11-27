import streamlit as st
from utility import APP_NAME, ai_in_live_mode, check_api_values
from authentication import is_user_authorized

st.set_page_config(page_title=f"{APP_NAME} Live Quiz", page_icon="✨", layout="wide")

st.markdown(f"# {APP_NAME} Live Quiz ✨")
st.write(
    f"""
    See {APP_NAME} in action against a live quiz!
    """
)

st.divider()

if check_api_values():
    # display the input field only for authenticated user
    # option to login not displayed here as unauthenticated users should only see the live video and no input option
    liveVideoURL = ''
    if is_user_authorized():
        getLiveVideoURL = st.text_input('Live Video Link')

        if st.button('Submit'):
            liveVideoURL = getLiveVideoURL

    if liveVideoURL:
        ai_in_live_mode(liveVideoURL)
