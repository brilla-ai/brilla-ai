from typing import Annotated

from uuid import uuid4

from fastapi import Depends, status

from helper.apply_pydantic_model import apply_pydantic_model

from helper.filter_none_values import filter_none_values

from core.reponse_model import BaseResponseModel

from models.liveVideo import LiveVideoEditLogCreateModel, LiveVideoEditLogReadModel, LiveVideoEditLogUpdateModel

from databaseStore.video.live_video_logs import LiveVideoEditLogRepository
from .interface.ILive_video_service import ILiveVideoService


class LiveVideoEditLogsService:
    def __init__(self, live_video_edit_logs_repository  :  Annotated[LiveVideoEditLogRepository,Depends(LiveVideoEditLogRepository)]):
        self.live_video_edit_logs_repository = live_video_edit_logs_repository

    def create_live_video_edit_logs(self, live_video_edit_logs: LiveVideoEditLogCreateModel):
        live_video_edit_logs_response  =  self.live_video_edit_logs_repository.create_live_video_edit_log(live_video_edit_logs) 
        if( live_video_edit_logs_response ):
            live_video_edit_logs_validated_response  =  apply_pydantic_model(LiveVideoEditLogReadModel, live_video_edit_logs_response)
            return  BaseResponseModel.create_response(live_video_edit_logs_validated_response, "Live video edit logs created successfully",status.HTTP_201_CREATED)  
        return  BaseResponseModel.create_response (None,"Live video edit logs not created",status.HTTP_400_BAD_REQUEST)
    
    def  get_live_video_edit_logs_by_live_video_id(self, live_video_id: uuid4):
        live_video_edit_logs_response  =  self.live_video_edit_logs_repository.get_edit_logs_by_live_video_id(live_video_id) 
        if( live_video_edit_logs_response ):
            live_video_edit_logs_validated_response  =  apply_pydantic_model(LiveVideoEditLogReadModel, live_video_edit_logs_response)
            return  BaseResponseModel.create_response(live_video_edit_logs_validated_response, "Live video edit logs fetched successfully",status.HTTP_200_OK)
        return  BaseResponseModel.create_response (None,"Live video edit logs not found",status.HTTP_404_NOT_FOUND)

    def get_lastest_edit_log_by_live_video_id(self, live_video_id: uuid4):
        edit_log_response = self.live_video_edit_logs_repository.get_last_edit_log_by_live_video_id(live_video_id)
        if(edit_log_response):
            edit_log_validated_response = apply_pydantic_model(LiveVideoEditLogReadModel, edit_log_response)
            return  BaseResponseModel.create_response(edit_log_validated_response, "Live video edit logs fetched successfully",status.HTTP_200_OK)
        return  BaseResponseModel.create_response (None,"Live video edit logs not found",status.HTTP_404_NOT_FOUND)
    
    def  update_live_video_edit_log(self, id: uuid4, live_video_edit_logs : LiveVideoEditLogUpdateModel):
        live_video_edit_logs = filter_none_values(live_video_edit_logs.model_dump())
        live_video_edit_logs_response  =  self.live_video_edit_logs_repository.update_live_video_edit_log(id, live_video_edit_logs) 
        if( live_video_edit_logs_response ):
            live_video_edit_logs_validated_response  =  apply_pydantic_model(LiveVideoEditLogUpdateModel, live_video_edit_logs_response)
            return  BaseResponseModel.create_response(live_video_edit_logs_validated_response, "Live video edit logs updated successfully",status.HTTP_200_OK)
        return  BaseResponseModel.create_response (None,"Live video edit logs not found",status.HTTP_404_NOT_FOUND)