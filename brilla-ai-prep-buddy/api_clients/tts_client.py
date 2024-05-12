import requests
import json


def get_tts_audio(text, base_url):
    TTS_API = base_url.rstrip('/') + "/synthesize-speech"

    if TTS_API is not None:
        payload = json.dumps({"text": text})
        response = requests.get(TTS_API.rstrip('/'), data=payload, verify=False)

        outfname = "tts_output.wav"
        if response.status_code == 200:
            with open(outfname, "wb+") as wav_file:
                wav_file.write(response.content)
        
    return outfname