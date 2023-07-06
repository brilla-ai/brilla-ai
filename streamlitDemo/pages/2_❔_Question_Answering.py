import streamlit as st
from utility import QA_QUESTION_BANK, realtime_question_answering, get_qa_api

st.set_page_config(page_title="Question Answering", page_icon="❔", layout="wide")

st.markdown("# Question Answering Demo❔")
st.write(
    """
    This demo illustrates a real time operation of the Question Answering Model of the NSMQ AI.
    """
)

if get_qa_api() == '-1':
    st.warning('Please setup the QA API on the API Setup page', icon="⚠️")

st.divider()

# text input for riddle
riddle = st.radio("Select A Riddle", (QA_QUESTION_BANK['riddle1'], QA_QUESTION_BANK['riddle2'], QA_QUESTION_BANK['riddle3']))

if st.button('Get AI Answer!'):
    # answer display
    realtime_question_answering(riddle)
