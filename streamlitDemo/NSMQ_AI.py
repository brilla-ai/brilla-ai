import streamlit as st
from authentication import authenticate

st.set_page_config(
    page_title="NSMQ AI",
    page_icon="👋",
    layout="wide"
)

welcomeCol, loginCol = st.columns([4,1])

with welcomeCol:
    st.write("# Welcome to NSMQ AI Demo! 👋")

    st.divider()

    st.markdown(
        """
        ### "Can an AI win Ghana’s National Science and Maths Quiz?". 
        
        This is the question posed by the NSMQ AI Grand Challenge 
        which is an AI Grand Challenge for Education using Ghana’s National 
        Science and Maths Quiz competition (NSMQ) as a case study. 
        
        The goal of nsmqai is to build an AI to compete live in the NSMQ competition 
        and win — performing better than the best contestants in all rounds and stages of the competition.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what NSMQ AI can do!
        """
    )

with loginCol:
    authenticate()
