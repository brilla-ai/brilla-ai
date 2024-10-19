from datetime import datetime

from typing import Annotated

from fastapi import Depends

from dateutil import parser

from services.videoService.video_service import LiveVideoService

from models.liveVideo import VideoStatus
from databaseStore.video.live_video import LiveVideoRepository
from core.live_video_repository_manager import get_live_video_repository_manager


live_video_service  = get_live_video_repository_manager()

def  check_and_update_live_video_status():
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
            print( "Background task", video.get("id"), "ended")
            print( status, "status")
        elif start_time and end_time and (start_time < current_time < end_time) and status != "live":
            live_video_service.update_live_video_status(video.get("id"), VideoStatus.live)
            print( "Background task", video.get("id"), "live")
        elif start_time and (start_time > current_time) and status != "upcoming":
            live_video_service.update_live_video_status(video.get("id"),  VideoStatus.upcoming)
            print( "Background task", video.get("id"), "upcoming")
