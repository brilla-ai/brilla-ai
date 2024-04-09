import streamlit as st
from authentication import authenticate
from utility import APP_NAME

st.set_page_config(
    page_title=f"{APP_NAME}",
    page_icon="👋",
    layout="wide"
)

welcomeCol, loginCol = st.columns([4,1])

with welcomeCol:
    st.write(f"# Welcome to {APP_NAME} Demo! 👋")

    st.divider()

    st.markdown(
        f"""
        ### "Can an AI win Ghana’s National Science and Maths Quiz?". 
        
        This is the question posed by the NSMQ AI Grand Challenge 
        which is an AI Grand Challenge for Education using Ghana’s National 
        Science and Maths Quiz competition (NSMQ) as a case study. 
        
        The goal of {APP_NAME} is to build an AI to compete live in the NSMQ competition 
        and win — performing better than the best contestants in all rounds and stages of the competition.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what {APP_NAME} can do!
        """
    )

with loginCol:
    authenticate()
