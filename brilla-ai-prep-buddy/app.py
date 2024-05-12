import streamlit as st
import time

from question_service import QuestionService
from utils import simulate_riddle, SessionState


API_URL = "https://731a-35-229-187-91.ngrok-free.app/"    # Always provide API url before running code.

st.set_page_config(page_title="Brilla-AI NSMQ Prep Buddy", page_icon="😎", layout="wide")

qs = QuestionService()
state = SessionState()

if state.riddle_id > len(qs):
        state.riddle_id = 1
        state.score = 0


st.markdown("# Brilla-AI NSMQ Prep Buddy 😎")
st.write(
    f"""
    Welcome to the Brilla-AI NSMQ Riddles Prep Buddy: Riddles Edition. 🎉

    Are you ready to test your scientific knowledge by answering real science riddles from the NSMQ?

    Let's Begin. Best of Luck! 😎💡
    """
)

st.divider()

st.write(
    f"""
    <h4><b>Score:</b> {state.score} out of {len(qs)} </h4>
    """,
    unsafe_allow_html=True
)

st.divider()

text_area = st.empty()
transcript_box = st.empty()
start_button = st.button("GET NEXT RIDDLE")
audio_place_holder = st.empty()

if start_button:
    riddle_id = state.riddle_id
    score = state.score

    score_from_riddle = simulate_riddle(qs=qs,
        riddle_id=riddle_id,
        text_area=text_area,
        transcript_box=transcript_box,
        audio_place_holder=audio_place_holder,
        base_url=API_URL
    )

    riddle_id = riddle_id + 1 if riddle_id < len(qs) else 1
    score += score_from_riddle
    state.write_state(riddle_id=riddle_id, score=score)
