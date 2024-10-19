from datetime import datetime

from typing import Annotated, List, Optional

from uuid import UUID, uuid4

from fastapi import Depends

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from models.liveVideo import LiveVideo, LiveVideoCreateModel, LiveVideoReadModel, LiveVideoUpdateStopStatusModel, VideoStatus

from database import get_db


class LiveVideoRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):   
        self.db  = db

    def  create_live_video(self, live_video: LiveVideoCreateModel) -> LiveVideoReadModel:
        print(live_video.model_dump())
        live_video = LiveVideo(**live_video.model_dump())
        self.db.add(live_video)
        self.db.commit()
        self.db.refresh(live_video)
        live_video_validated = LiveVideoReadModel.from_orm(live_video)
        return live_video_validated
    
    def get_live_video_by_id(self, id: UUID) -> Optional[LiveVideoReadModel]:
        response =  self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).first()
        return  LiveVideoReadModel.from_orm(response)

    def get_all_live_video(self) -> Optional[List[LiveVideoReadModel]] :
        live_video_response =  self.db.query(LiveVideo).filter(LiveVideo.deleted_at == None).order_by(LiveVideo.created_at.desc()).all()
        live_video_response = jsonable_encoder([LiveVideoReadModel.from_orm(video) for video in live_video_response])
        return live_video_response
   
    
    def update_live_video(self, id: UUID, live_video : dict ) -> LiveVideoReadModel:
        self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).update( live_video, synchronize_session='evaluate')
        self.db.commit()
        
        # self.db.refresh(live_video)
        response  =  jsonable_encoder(LiveVideoReadModel.from_orm(live_video))
        return response
    

    def update_live_video_status(self, id: UUID, status: VideoStatus) -> Optional[LiveVideoReadModel]:
        live_video = self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).update({'status': status.value}, synchronize_session='evaluate')
        
        print( live_video, "live_video")
        if not live_video:
            return None
        
        self.db.commit()
        if live_video:
            response  =  self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).first()
            return response
        return None 
    
    def stop_live_video_update(self, id: UUID, stop_status: bool) -> Optional[LiveVideoReadModel]:
        live_video = self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).first()
        
        if not live_video:
            return None
        
        stop_time = datetime.now() if stop_status else None

        live_video.stop_time = stop_time

        self.db.commit()

        self.db.refresh(live_video)

        live_video_validated = jsonable_encoder(LiveVideoReadModel.from_orm(live_video))

        return live_video_validated
    

    def delete_live_video(self, id: UUID):
        self.db.query(LiveVideo).filter(LiveVideo.id == id, LiveVideo.deleted_at == None).update({'deleted_at': datetime.utcnow()}, synchronize_session='evaluate')
        self.db.commit()
        return True