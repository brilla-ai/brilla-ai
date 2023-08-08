# About Speech-To-Text
Speech-To-Text (STT) team works on:
- Real-time speech-to-text system with low latency, and robust against noise, and delineates each clue
- Baseline results of at least 5 state-of-the-art models using the transcript from the Data Curation team and audios from the Data Preprocessing team
- Trained model, code, and evaluation results

## Using the STT_Inference_API_Server notebook
Follow the description below: 

## Introduction
This script allows you to create a public API that enables audio file transcription and/or real-time transcription in our Streamlit-built application. The API can be easily integrated into the Streamlit application, providing a seamless and user-friendly experience for transcribing audio.

## Requirements
Before running the script, you will need to have the following:

1. A valid [ngrok](https://ngrok.com/) account to create a public URL for your API.
2. An authentication token provided by ngrok, which you will copy into the code.

## Setup
Follow these steps to set up the STT API:

1. Create an account on [ngrok](https://ngrok.com/) to obtain your authentication token.
2. Copy the authentication token provided by ngrok and paste it into the designated section of the code. 
3. Run the entire script and copy the generated public URL.
4. Paste the URL into the "Speech To Text" section of the the API Setup Page, as shown below.
![image](https://github.com/nsmq-ai/nsmqai/assets/92085084/aee5747b-2116-48e1-877a-e3eb37080923)

