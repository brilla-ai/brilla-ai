# Question-Answering
The Question-Answering team works on:
- Question answering of riddles (after each clue along with confidence estimate) using relevant knowledge source.
- Baseline results of at least 5 state-of-the-art models using the transcript from the Data Curation team for each subsequent clue.
- Trained model, code, and evaluation results.

## Using the QAML Inference API Server notebook
To use the QA system, follow the instructions below:

## Live Question-Answering
The Live QA system is designed to answer questions in real-time during NSMQ competitions. The system is integrated into the Streamlit application and can be accessed through the following steps:

1. Access the Streamlit Application
Launch the NSMQ AI Project Streamlit application, where you'll find the live QA system (refer to the Streamlit Documentation).
2. Input Clues
Provide the relevant clues or questions within the application to initiate the QA process.
3. Real-Time Answers
The system uses the Mistral and (optional) ChatGPT models to generate real-time answers.
The generated answers are displayed within the application.

## Demo Question-Answering
The QA system also supports demo question-answering for demonstration purposes. To use the demo QA feature:

1. Access the Demo Section
Navigate to the demo section of the Streamlit application.
2. Input Riddles
Enter riddles or questions that you'd like the QA system to answer.
3. Demo Answers
The system uses the Mistral model to generate answers for the provided riddles.
The answers are displayed within the application.

## Requirements
To use the QA System, you will need the following:

1. A valid [ngrok](https://ngrok.com/) account.
2. An authentication token provided by ngrok, which you should put in the secrets section of the notebook.
3. [Optional] An API Key from OpenAI (https://platform.openai.com/account/api-keys) if you wish to use ChatGPT as well.
4. Refer to the Web App documentation for steps on how to start and use the Web App.

## Integration with the STT System
For STT integration details, refer to the STT documentation.
