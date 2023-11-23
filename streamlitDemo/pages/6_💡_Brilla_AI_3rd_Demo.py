import streamlit as st
from utility import APP_NAME, ai_in_live_demo_mode, DEMO_AUDIO_11_PATH, DEMO_VIDEO_11_PATH

st.set_page_config(page_title=f"{APP_NAME} 3rd Demo", page_icon="💡", layout="wide")

st.markdown(f"# {APP_NAME} 3rd Demo💡")
st.write(
    f"""
    This demo illustrates a real time operation of all components of {APP_NAME}. Enjoy!
    """
)

st.divider()

# display end to end flow
ai_in_live_demo_mode(DEMO_VIDEO_11_PATH, DEMO_AUDIO_11_PATH)
