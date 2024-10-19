import requests
import json
import base64

def get_stt_transcript(audio_file, base_url):
    STT_API_ENDPOINT = base_url.rstrip('/') + '/get-transcript'
    if STT_API_ENDPOINT:
        with open(audio_file, "rb") as f:
            audio_bytes = f.read()
            bytes_data = base64.b64encode(audio_bytes).decode()

            payload = {"data": bytes_data, "filename": "temp_audio.wav"}
            payload = json.dumps(payload)

            response = requests.get(STT_API_ENDPOINT, data=payload)

            transcript = ''
            if response.status_code == 200:
                response_data = response.json()
                if response_data.get('transcript') is not None:
                    transcript = response_data.get('transcript')
    
    return transcript