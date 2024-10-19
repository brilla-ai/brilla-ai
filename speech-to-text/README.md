# About Speech-To-Text
Speech-To-Text (STT) team works on:
- Real-time speech-to-text system with low latency, and robust against noise, and delineates each clue
- Baseline results of at least 5 state-of-the-art models using the transcript from the Data Curation team and audios from the Data Preprocessing team
- Trained model, code, and evaluation results

## Using the STT Starter notebook
The notebook simulates how to perform speech transcription using distil-whisper. The notebook demonstrates two methods of transcribing, one suitable for short-length audios and the other for long-length audios. The audio files referred to in the notebook can be found in the "Starter notebook audios" folder. Ensure you have downloaded the audios and loaded them into your notebook to run.

## Using the STT_Inference_API_Server notebook
Follow the description below: 

## Introduction
This script allows you to create a public API that enables audio file transcription and/or real-time transcription in our Streamlit-built application. The API can be easily integrated into the Streamlit application, providing a seamless and user-friendly experience for transcribing audio.

## Revisioning
The earlier version of the STT_Inference_API_Server notebook performed only transcription of audios. However, Version 2 incorporates a number of functionalities in addition to audio transcription, specific to the NSMQ competition. The different functionalities are briefly described below:\
a) Start of new riddle detector\
b) Riddle clue classifier\
c) Place holder for all identified riddle clues within a riddle\
d) Counter for individual clues in transcripts\
e) End of current riddle detector

Version 2 workflow seeks to now transcribe a given audio, then, determine whether there is any indicator of a new riddle. Once a new riddle is identified, the subsequent transcripts will be filtered for clues. The clues will be concatenated with any other captured clues in the subsequent transcripts until the start of a new riddle is identified. The sequence is repeated for every new riddle until the end of the contest. The counter and end of riddle detector features enable functionality within the Question-Answering model.

## Requirements
Before running the script, you will need to have the following:

1. A valid [ngrok](https://ngrok.com/) account.
2. An authentication token provided by ngrok, which you should put in the secrets section of the notebook

## Setup
Follow these steps to set up the STT API:

1. Create an account on [ngrok](https://ngrok.com/) to obtain your authentication token.
2. Copy the authentication token provided by ngrok and paste it into the designated section of the code. 
3. Run the entire script and copy the generated public URL.
4. Paste the URL into the "Speech To Text" section of the the API Setup Page, as shown below.
![image](https://github.com/brilla-ai/brilla-ai/assets/92085084/aee5747b-2116-48e1-877a-e3eb37080923)

