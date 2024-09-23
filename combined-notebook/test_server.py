import requests
import json
import base64


URL = "https://6913-35-240-168-164.ngrok-free.app/"


# Test TTS
def test_tts() -> None:
    # Create payload
    payload = {"text": "animal", "flag": 0}

    # Send POST request to TTS endpoint on server
    response = requests.get(
        f"{URL.rstrip('/')}/tts",
        data=json.dumps(payload)
    )

    if response.status_code == 200:
        # Write synteshized audio to disk
        with open("./tts_test_response.wav", "wb") as f:
            f.write(response.content)

        print("Audio saved to ./tts_test_response.wav")
    else:
        print("ERROR: Status Code: {response.status_code}")


# Test STT
def test_stt() -> None:
    audio_file_path = "./combined-notebook/test-riddle-trimmed.wav"
    # Read the audio file in binary mode
    with open(audio_file_path, 'rb') as audio_file:
        audio_bytes = audio_file.read()

    # Encode the audio bytes to base64
    encoded_audio = base64.b64encode(audio_bytes).decode('utf-8')

    # Create the payload with base64-encoded data
    payload = {
        "data": encoded_audio,
        "filename": audio_file_path.split("/")[-1],
        "current_round": 5
    }

    # Send the request with JSON payload to the /get-transcript endpoint
    response = requests.post(
        f"{URL.rstrip('/')}/get-transcript",
        json=payload  # Sending payload as JSON
    )

    if response.status_code == 200:
        # Print the response (transcript and pause detection result)
        result = response.json()
        print(f"Transcript: {result.get('transcript')}")
        print(f"Is pause detected: {result.get('is_pause_detected')}")
    else:
        print("ERROR: Status Code: {response.status_code}, Error: {response.text}")


# QA Test for Round 4
def test_qa_round_4():
    payload = {
        "currentRound": 4,
        "extractedQuestion": "Hydrogen has atomic number 3",
    }

    # Send the request
    response = requests.get(
        f"{URL.rstrip('/')}/answer",
        json=payload
    )

    # Verify response
    if response.status_code == 200:
        answer = response.json()
        print(f"Round 4 Answer: {answer.get('answerText')}")
    else:
        print(f"ERROR: Status Code: {response.status_code}, Response: {response.text}")


# Test for Round 5
def test_qa_round_5():
    payload = {
        "currentRound": 5,
        "clues": "I am an organ in the human body",
        "clues_count": 1,
        "is_start_of_riddle": False,
        "is_end_of_riddle": True
    }

    # Send the request
    response = requests.get(
        f"{URL.rstrip('/')}/answer",
        json=payload
    )

    # Verify response
    if response.status_code == 200:
        answer = response.json()
        print(f"Round 5 Answer: {answer.get('answerText')}")
    else:
        print(f"ERROR: Status Code: {response.status_code}, Response: {response.text}")


# Test for Round 4
def test_qe_round_4():
    payload = {
        "transcript": "Hydrogen has atomic number 3",
        "current_round": 4,
        "pause_detected": False
    }

    # Send the request
    response = requests.get(
        f"{URL.rstrip('/')}/qe",
        json=payload
    )

    # Verify response
    if response.status_code == 200:
        result = response.json()
        print(f"Round 4 Extracted Question: {result.get('extractedQuestion')}")
    else:
        print(f"ERROR: Status Code: {response.status_code}, Response: {response.text}")


# Test for Round 5
def test_qe_round_5():
    payload = {
        "transcript": "I am a concept in different science sub-disciplines",
        "current_round": 5,
        "pause_detected": False  # Pause is irrelevant for round 5
    }

    # Send the request
    response = requests.get(
        f"{URL.rstrip('/')}/qe",
        json=payload
    )

    # Verify response
    if response.status_code == 200:
        result = response.json()
        print(f"Round 5 Clues: {result.get('clues')}")
        print(f"Clue Count: {result.get('clue_count')}")
        print(f"Is Start of Riddle: {result.get('is_start_of_riddle')}")
    else:
        print(f"ERROR: Status Code: {response.status_code}, Response: {response.text}")


if __name__ == "__main__":
    # TTS Test
    print("Testing TTS")
    test_tts()

    # STT Test
    print("\nTesting STT")
    test_stt()

    # Test QA Round 4
    print("\nTesting QA Round 4")
    test_qa_round_4()

    # Test QA Round 5
    print("\nTesting QA Round 5")
    test_qa_round_5()

    # Test QE Round 4
    print("\nTesting QE Round 4")
    test_qe_round_4()

    # Test QE Round 5
    print("\nTesting QE Round 5")
    test_qe_round_5()
