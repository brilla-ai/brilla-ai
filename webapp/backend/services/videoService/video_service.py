from datetime import datetime

from typing import Annotated

from uuid import UUID

import logging

from fastapi import Depends, status

from helper.filter_none_values import filter_none_values

from core.websocket_connection_manager import get_connection_manager

from websocket.websocket import ConnectionManager

from .interface.ILive_video_service import ILiveVideoService


from .live_video_edit_logs import LiveVideoEditLogsService

from core.reponse_model import BaseResponseModel

from models.liveVideo import LiveVideoCreateModel, LiveVideoEditLogCreateModel, LiveVideoUpdateModel, LiveVideoUpdateStopStatusModel, VideoStatus

from databaseStore.video.live_video import LiveVideoRepository


class  LiveVideoService(ILiveVideoService):
    def __init__(self, live_video_repository: Annotated[LiveVideoRepository, Depends(LiveVideoRepository)], live_video_edit_logs_service : Annotated[LiveVideoEditLogsService, Depends(LiveVideoEditLogsService)], command_manager : Annotated[ConnectionManager, Depends(get_connection_manager)]):
        self.live_video_repository = live_video_repository
        self.live_video_edit_logs_service  = live_video_edit_logs_service
        self.connection_manager = command_manager


    def  create_live_video(self, live_video: LiveVideoCreateModel, user_id : UUID):
        live_video_response  =  self.live_video_repository.create_live_video(live_video) 
        if( live_video_response ):
            logging.info("Create_Live_Video: Live video created successfully")

            print(live_video_response, "live_video_validated_response")
            # Add log entry
            self.__create_live_video_log(user_id, live_video_id=live_video_response.id)
            
            return  BaseResponseModel.create_response(live_video_response, "Live video created successfully",status.HTTP_201_CREATED)
        
    def  update_live_video(self, id: UUID, live_video : LiveVideoUpdateModel, user_id : UUID):
        live_video = filter_none_values(live_video.model_dump())
        print(live_video.pop("id"), "live_video")
        live_video_response  =  self.live_video_repository.update_live_video(id, live_video) 
        if( live_video_response ):

            #  add an entry to the log 
            print(live_video_response, "live_video_response")
            self.__create_live_video_log(user_id, id)

            response =  BaseResponseModel.create_response(live_video_response, "Live video updated successfully",status.HTTP_200_OK)
            if(live_video.get("status") == VideoStatus.live):
                self.connection_manager.send_message_to_group("live_video", response)
            return response 

    def  get_live_video_by_id(self, id: UUID):
        live_video_response  =  self.live_video_repository.get_live_video_by_id(id) 
        if( live_video_response ):
            print(live_video_response, "live_video_response")
            return  BaseResponseModel.create_response(live_video_response.dict(), "Live video fetched successfully",status.HTTP_200_OK)
        return  BaseResponseModel.create_response (None,"Live video not found",status.HTTP_404_NOT_FOUND)
    def  get_all_live_video(self):
        print( "service called" )
        live_video_response  =  self.live_video_repository.get_all_live_video() 
        if( live_video_response ):
            return  BaseResponseModel.create_response(live_video_response, "Live video fetched successfully",status.HTTP_200_OK)
        
    async def delete_live_video(self, id: UUID, user_id : UUID):
        delete_reponse  =  self.live_video_repository.delete_live_video(id) 
        if( delete_reponse ):
            self.__create_live_video_log(user_id, id)
            delete_reponse = BaseResponseModel.create_response (None,"Live video deleted successfully",status.HTTP_200_OK)  
            self.connection_manager.send_message_to_group("live_video", delete_reponse)
            return delete_reponse
        delete_response_error =  BaseResponseModel.create_response (None,"Live video not found",status.HTTP_404_NOT_FOUND) 
        await self.connection_manager.send_message_to_group("live_video", delete_reponse)
        return delete_response_error
    

    async def  stop_live_video_update(self, id: UUID, user_id : UUID, stop_status: LiveVideoUpdateStopStatusModel):
        live_video_response  =  self.live_video_repository.stop_live_video_update(id, stop_status) 
        if( live_video_response ):
            # live_video_validated_response  =  apply_pydantic_model(LiveVideoReadModel, live_video_response)
            
            #  add an entry to the log 
            self.__create_live_video_log(user_id, id)

            response =   BaseResponseModel.create_response(live_video_response, "Live video updated successfully",status.HTTP_200_OK)
            await self.connection_manager.send_message_to_group("live_video", response)
            return response
        error_response = BaseResponseModel.create_response(None, "Live video not found", status.HTTP_404_NOT_FOUND)
        await self.connection_manager.send_message_to_group("live_video", error_response)
        return error_response
    


    def __create_live_video_log(self, user_id : UUID, live_video_id  : UUID):
         #  add an entry to the log 
            log_entry  = LiveVideoEditLogCreateModel( user_id= user_id, updated_at= datetime.utcnow() ,live_video_id =live_video_id)

            live_video_edit_logs = self.live_video_edit_logs_service.create_live_video_edit_logs(log_entry)
            print(live_video_edit_logs)
            if(live_video_edit_logs.get("status_code") != status.HTTP_201_CREATED):
                logging.info("Create_Live_Video: Could not create audit log")

            logging.info("Create_Live_Video: Audit log created successfully")


    def get_status_live_video(self, video_status: VideoStatus):
        status_live_video = self.live_video_repository.get_live_video_status(video_status)
        if (not status_live_video):
            return BaseResponseModel.create_response(None, "Live video not found", status.HTTP_404_NOT_FOUND)
        return BaseResponseModel.create_response(status_live_video, "Live video fetched successfully",status.HTTP_200_OK)
