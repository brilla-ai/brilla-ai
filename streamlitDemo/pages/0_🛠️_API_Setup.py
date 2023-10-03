import streamlit as st
from utility import INDIVIDUAL_API_SETUP, ALL_IN_ONE_API_SETUP, apiSetupPageOperation
from authentication import is_user_authorized, authenticate

st.set_page_config(page_title="API Setup", page_icon="🎙️", layout="wide")

apiSetupCol, loginCol = st.columns([4,1])

# display pages only for authenticated user
with apiSetupCol:
    if is_user_authorized():
        st.markdown("# API Setup 🛠️")
        st.write(
            """
            Set up API servers to handle the Machine Learning tasks. Options are an API to handle all tasks or individual APIs for each task.
            """
        )

        allInOneURLSetup, individualURLSetup = st.tabs(["ALL IN ONE API", "INDIVIDUAL APIs"])

        with allInOneURLSetup:
            apiSetupPageOperation(ALL_IN_ONE_API_SETUP)

        with individualURLSetup:
            apiSetupPageOperation(INDIVIDUAL_API_SETUP)
    else:
        st.markdown("# Access Denied")
        st.write("Log in with appropriate credentials")

with loginCol:
    authenticate()
