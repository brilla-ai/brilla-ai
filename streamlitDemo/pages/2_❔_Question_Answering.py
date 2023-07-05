import streamlit as st
from utility import QA_QUESTION_BANK, get_qa_answer

st.set_page_config(page_title="Question Answering", page_icon="❔", layout="wide")

st.markdown("# Question Answering Demo❔")
st.write(
    """
    This demo illustrates a real time operation of the Question Answering Model of the NSMQ AI.
    """
)

st.divider()

# text input for riddle
riddle = st.radio("Select A Riddle", (QA_QUESTION_BANK['riddle1'], QA_QUESTION_BANK['riddle2'], QA_QUESTION_BANK['riddle3']))

# answer display
answerBoxText = ''

if st.button('Get AI Answer!'):
    with st.spinner("Working On Answer!"):
        answerBoxText = get_qa_answer(riddle)
    answerBox = st.empty()
    answerBox.text_area("Answer", answerBoxText, height = 10, label_visibility="hidden")
