from typing import Annotated

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from models.liveVideo import LiveVideoCreateModel, LiveVideoUpdateModel

from models.user import ReadUserModel, Role

from services.userService.oauth import get_current_user

from services.videoService.video_service import LiveVideoService

live_video = APIRouter(tags=["live_video"], prefix="/video")


@live_video.get("/all")
def get_all_live_video( live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    return live_video_service.get_all_live_video()


@live_video.get("/{id}")
def get_live_video_by_id(id:  UUID, live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    return live_video_service.get_live_video_by_id(id)


@live_video.delete("/{id}")
async def delete_live_video(id:  UUID, live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        live_video_response = await live_video_service.delete_live_video(id,  current_user.id)
        return live_video_response
    raise HTTPException(status_code=401, detail="Unauthorized")

@live_video.post("/{id}/stop")
async def stop_live_video_update(id:  UUID, status: bool ,  live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return await  live_video_service.stop_live_video_update(id, current_user.id, status)
    raise HTTPException(status_code=401, detail="Unauthorized")

@live_video.put("/{id}")
async def update_live_video(live_video_data: LiveVideoUpdateModel, live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return await live_video_service.update_live_video(live_video_data.id, live_video_data, current_user.id)
    raise HTTPException(status_code=401, detail="Unauthorized")

@live_video.post("/create")
def create_live_video(live_video_data: LiveVideoCreateModel, live_video_service:  Annotated[LiveVideoService, Depends(LiveVideoService)], current_user:  ReadUserModel = Depends(get_current_user)):
    if( current_user.role == Role.admin or  current_user.role == Role.moderator):
        return live_video_service.create_live_video(live_video_data, current_user.id)
    raise HTTPException(status_code=401, detail="Unauthorized")
