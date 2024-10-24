from typing import Annotated, Dict, Union
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder

from core.websocket_connection_manager import get_connection_manager
from websocket.websocket import ConnectionManager

import base64
import logging

from pydub import AudioSegment
from pydub.playback import play

ml_layer = APIRouter(tags=["ml_layer"])


@ml_layer.post("/receive-from-brilla-ai")
async def receive_from_brilla_ai(payload: Dict[str, Union[str, bytes]], connection_manager: Annotated[ConnectionManager, Depends(get_connection_manager)]):
    try:
        # Parse the incoming payload data
        # payload = {"transcript": "qwertyui", "extracted_question": "asdfghjk"}
        
        # Log received payload
        # logging.info(f"Received payload: {payload}")

        # Determine which kind of payload it is based on the fields
        json_response = ""
        if ("generated_audio" not in payload):
            json_response = jsonable_encoder(payload)
            if 'transcript' in payload:
                # logging.info("Handling STT Data")
                await connection_manager.send_message_to_group("live_video", json_response)
                return {"message": "STT Data received", "data": payload}
            elif 'extracted_question' in payload:
                # logging.info("Handling QE Data")
                await connection_manager.send_message_to_group("live_video", json_response)
                return {"message": "QE Data received", "data": payload}
            elif payload.get('answer_text'):
                await connection_manager.send_message_to_group("live_video", json_response)
                # logging.info("Handling QA Data")
                return {"message": "QA Data received", "data": payload}
        elif 'generated_audio' in payload:
            # logging.info("Handling TTS Data")
            value = payload.get("generated_audio")
            # print("TTS_PAYLOAD", payload)
            
            # if isinstance(value, bytes):
                #await connection_manager.send_message_to_group("live_video", value, "bytes")

                # create an audio file
            outputFileName = "tts_output.wav"

            processed_payload = base64.b64decode(value)
            with open(outputFileName, "wb+") as file:
                file.write(processed_payload)

            # play the audio
            # playsound(outputFileName)
            song = AudioSegment.from_wav(outputFileName)
            play(song)

            return {"message": "TTS Data received"}
        else:
            # logging.warning("Unknown payload type")
            return {"error": "Unknown payload type"}, 400

    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return {"error": "Failed to process the request"}, 500
    


@ml_layer.get("/play-audio")
def play_audio():
    song = AudioSegment.from_wav("output.wav")
    print('playing sound using  pydub')
    play(song)
    # playsound('../output.wav')