from typing import Annotated, Dict, Optional, Union
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException, Request

from core.ml_layer import process_audio_from_video
from models.aiOperations import AIOperationsUpdateModel, VideoUrl

from services.aiOperationsService.ai_operations import AIOperationsService

from services.userService.oauth import get_current_user

from models.user import ReadUserModel, Role
from core.websocket_connection_manager import get_connection_manager
from websocket.websocket import ConnectionManager

from fastapi.encoders import jsonable_encoder

import base64
import logging



ai_operations = APIRouter(tags=["ai_operations"], prefix="/operations")

videos = ["https://www.youtube.com/watch?v=2AUpiVB6zA4&ab_channel=NSMQAI"]

BASE_URL = "https://3143-34-87-17-167.ngrok-free.app/"

AUDIO_CHUNKS_DIR_PATH = "cache/audio_chunks"


@ai_operations.get("/operation")
def get_ai_operation( ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return ai_operations_service.get_ai_operation()
    raise HTTPException(status_code=401, detail="Unauthorized")


@ai_operations.put("/operation/{id}")
def update_ai_operations(id: UUID, ai_operations : AIOperationsUpdateModel, ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return ai_operations_service.update_ai_operations(id, ai_operations)
    raise HTTPException(status_code=401, detail="Unauthorized")



@ai_operations.get("/start-audio-processsing")
def start_audio_processing():
    try:
        # extract audio from video
        # video_to_process = videos[0]
        # process and send to ML layer
        process_audio_from_video(videos[0], AUDIO_CHUNKS_DIR_PATH, BASE_URL)

    except Exception as e:
        return {"message": str(e)}
