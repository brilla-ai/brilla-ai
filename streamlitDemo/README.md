# NSMQ AI Workshop Demo

## Setup
- The code can be run locally. Follow steps here to setup a python environment for streamlit https://docs.streamlit.io/library/get-started/installation
- Install whisper in the virtual python environment following steps here https://pypi.org/project/openai-whisper
- Install below dependencies in the virtual python environment as well using pip or preferred package manager
  - `pip install -U openai-whisper`
  - `pip install pydub`
  - `pip install audioread`
  - `pip install SpeechRecognition`
  - `pip install pyaudio`

## Deploy
- From the local directory, run command from terminal `streamlit run NSQM_AI.py`
- WebApp will be deployed at `http://localhost:8501/`
