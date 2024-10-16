from typing import Annotated

from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException

from services.userService.oauth import get_current_active_user

from models.user import ReadUserModel, Role

from services.videoService.live_video_edit_logs import LiveVideoEditLogsService


live_video_edit_logs = APIRouter(tags=["live_video_edit_logs"], prefix="/video")


@live_video_edit_logs.get("/edit_logs")
async def get_live_video_edit_logs_by_live_video_id(live_video_id: UUID, live_video_edit_logs_service:Annotated[LiveVideoEditLogsService, Depends(LiveVideoEditLogsService)], current_user : Annotated[ReadUserModel, Depends(get_current_active_user)]):
    live_video_edit_logs = live_video_edit_logs_service.get_live_video_edit_logs_by_live_video_id(live_video_id)
    if( current_user.role == Role.admin or   current_user.role == Role.moderator):
        return live_video_edit_logs

    raise HTTPException(status_code=401, detail="Unauthorized")


@live_video_edit_logs.get("/edit_logs/last")
async def get_last_live_video_edit_log(live_video_id: UUID, live_video_edit_logs_service: Annotated[LiveVideoEditLogsService, Depends(LiveVideoEditLogsService)], current_user : Annotated[ReadUserModel, Depends(get_current_active_user)]):
    live_video_edit_log = live_video_edit_logs_service.get_lastest_edit_log_by_live_video_id(live_video_id)
    if( current_user.role == Role.admin or   current_user.role == Role.moderator):
        return live_video_edit_log

    raise HTTPException(status_code=401, detail="Unauthorized")


                          