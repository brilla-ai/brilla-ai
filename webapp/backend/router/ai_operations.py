from typing import Annotated, Dict, Optional, Union
from uuid import UUID


from fastapi import APIRouter, Depends, HTTPException, Request

from core.ml_layer import process_audio_from_video
from models.aiOperations import AIOperationsUpdateModel, VideoUrl

from services.aiOperationsService.ai_operations import AIOperationsService
from services.videoService.video_service import LiveVideoService

from services.userService.oauth import get_current_user

from models.user import ReadUserModel, Role
from core.websocket_connection_manager import get_connection_manager
from models.liveVideo import VideoStatus
from websocket.websocket import ConnectionManager

from fastapi.encoders import jsonable_encoder

import base64
import logging
import os



ai_operations = APIRouter(tags=["ai_operations"], prefix="/operations")

BASE_URL = os.getenv("ML_API_URL")

AUDIO_CHUNKS_DIR_PATH = "cache/audio_chunks"


@ai_operations.get("/operation")
def get_ai_operation( ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return ai_operations_service.get_ai_operation()
    raise HTTPException(status_code=401, detail="Unauthorized")


@ai_operations.put("/operation/{id}")
async def update_ai_operations(id: UUID, ai_operations : AIOperationsUpdateModel, ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)], current_user: Annotated[ReadUserModel, Depends(get_current_user)]):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return await ai_operations_service.update_ai_operations(id, ai_operations)
    raise HTTPException(status_code=401, detail="Unauthorized")



@ai_operations.get("/start-audio-processing")
async def start_audio_processing(video_service: Annotated[LiveVideoService, Depends(LiveVideoService)], ai_operations_service: Annotated[AIOperationsService, Depends(AIOperationsService)]):
    try:
        # extract audio from video
        # video_to_process = videos[0]
        # process and send to ML layer
        video = video_service.get_status_live_video(VideoStatus.live)
        ai_operations = ai_operations_service.get_ai_operation()
        stages = {
            "STAGE1": 1,
            "STAGE2": 2,
            "STAGE3": 3,
            "STAGE4": 4,
            "STAGE5": 5
        }
        current_stage = stages[ai_operations.get("data").get("stage_round")]
        print("CURRENT STAGE",current_stage)
        print("VIDEO",video)
        if(video.get("status_code") != 200):
            return video
        process_audio_from_video(video.get("data").get("video_link"), AUDIO_CHUNKS_DIR_PATH, BASE_URL, current_stage)
        



    except Exception as e:
        return {"message": str(e)}
