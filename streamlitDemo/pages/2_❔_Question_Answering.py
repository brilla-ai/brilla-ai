import streamlit as st
from utility import DEMO_QA_QUESTION, DEMO_QA_ANSWER, get_qa_answer

st.set_page_config(page_title="Question Answering", page_icon="❔", layout="wide")

st.markdown("# Question Answering Demo❔")
st.write(
    """
    This demo illustrates a real time operation of the Question Answering Model of the NSMQ AI.  Steps:
    - Enter A riddle 
    - Click "Get AI Answer!"
    - See the real time generated answer
    
    Enjoy!
    """
)

st.divider()

# text input for riddle
riddle = st.text_area("Enter A Riddle", DEMO_QA_QUESTION['text'], placeholder = DEMO_QA_QUESTION['text'], height = 80)

# answer display
answerBoxText = ''

if st.button('Get AI Answer!'):
    # TODO: get actual answer from API and display
    #st.write(get_qa_answer(riddle))
    answerBoxText = DEMO_QA_ANSWER['answer']

answerBox = st.empty()
answerBox.text_area("Answer", answerBoxText, height = 10)
