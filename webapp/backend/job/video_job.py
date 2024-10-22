from datetime import datetime

from typing import Annotated

from fastapi import Depends, status as fastapi_status

from dateutil import parser

from services.videoService.video_service import LiveVideoService

from models.liveVideo import LiveVideoReadModel, VideoStatus
from databaseStore.video.live_video import LiveVideoRepository
from core.live_video_repository_manager import get_live_video_repository_manager

from core.websocket_connection_manager import get_connection_manager
from fastapi.encoders import jsonable_encoder

from core.reponse_model import BaseResponseModel


live_video_service  = get_live_video_repository_manager()
connection_manager = get_connection_manager()

async def  check_and_update_live_video_status():
    print( "Background service running...")
    current_time  = datetime.utcnow()
    videos  = live_video_service.get_all_live_video()

    for video in videos:
        end_time = parser.isoparse(video.get("end_time")) if video.get("end_time") else None
        start_time = parser.isoparse(video.get("start_time")) if video.get("start_time") else None
        status = video.get("status")

        if end_time and (end_time < current_time) and (status != "ended") :
            print( (end_time < current_time) )
            print( status == str(VideoStatus.ended), "status")
            live_video_service.update_live_video_status(video.get("id"),  VideoStatus.ended)

            new_video = live_video_service.get_live_video_by_id(video.get("id"))
            json_video = jsonable_encoder(LiveVideoReadModel.from_orm(new_video.dict()))
            response = BaseResponseModel.create_response(json_video, "Video updated successfully", fastapi_status.HTTP_200_OK)
            await connection_manager.send_message_to_group("live_video", {"type": 1, "target": "video_ended", "arguments": response})

            await connection_manager.send_message_to_group("admin_videos", {"type": 1, "target": "update_video", "arguments": response})
            print( "Background task", video.get("id"), "ended")
            print( status, "status")
        elif start_time and end_time and (start_time < current_time < end_time) and status != "live":
            live_video_service.update_live_video_status(video.get("id"), VideoStatus.live)

            new_video = live_video_service.get_live_video_by_id(video.get("id"))
            json_video = jsonable_encoder(LiveVideoReadModel.from_orm(new_video.dict()))
            response = BaseResponseModel.create_response(json_video, "Video updated successfully", fastapi_status.HTTP_200_OK)
            await connection_manager.send_message_to_group("live_video", {"type": 1, "target": "video_started", "arguments": response})

            await connection_manager.send_message_to_group("admin_videos", {"type": 1, "target": "update_video", "arguments": response})
            print( "Background task", video.get("id"), "live")
        elif start_time and (start_time > current_time) and status != "upcoming":
            live_video_service.update_live_video_status(video.get("id"),  VideoStatus.upcoming)
            new_video = live_video_service.get_live_video_by_id(video.get("id"))

            json_video = jsonable_encoder(LiveVideoReadModel.from_orm(new_video.dict()))
            response = BaseResponseModel.create_response(json_video, "Video updated successfully", fastapi_status.HTTP_200_OK)

            await connection_manager.send_message_to_group("admin_videos", {"type": 1, "target": "update_video", "arguments": response})
            print( "Background task", video.get("id"), "upcoming")
