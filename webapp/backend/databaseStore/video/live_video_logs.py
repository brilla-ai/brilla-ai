from uuid import uuid4

from sqlalchemy.orm import Session

from typing import Annotated, List

from fastapi import Depends

from database import get_db

from models.liveVideo import LiveVideoEditLog, LiveVideoEditLogCreateModel, LiveVideoEditLogReadModel


class LiveVideoEditLogRepository:
    def __init__(self, db: Annotated[Session, Depends(get_db)]):   
        self.db  = db

    def create_live_video_edit_log(self, live_video_edit_log: LiveVideoEditLogCreateModel) -> LiveVideoEditLogReadModel:
        live_video_edit_log = LiveVideoEditLog(**live_video_edit_log.model_dump())
        self.db.add(live_video_edit_log)
        self.db.commit()
        self.db.refresh(live_video_edit_log)
        return live_video_edit_log
    
    def  update_live_video_edit_log(self, id: uuid4, live_video_edit_log : dict ) -> LiveVideoEditLogReadModel:
        self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.id == id).update( live_video_edit_log, synchronize_session='evaluate')
        self.db.commit()
        self.db.refresh(live_video_edit_log)
        return live_video_edit_log
    
    def get_edit_log_by_id(self, id: uuid4) -> LiveVideoEditLogReadModel:
        return self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.id == id).first()
    
    def  delete_live_video_edit_log(self, id: uuid4):
        self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.id == id).delete()
        self.db.commit()
        if( self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.id == id).first() ):
            return False
        return True
    
    def get_edit_logs_by_live_video_id(self, live_video_id: uuid4) -> List[LiveVideoEditLogReadModel]:
        return self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.live_video_id == live_video_id).all()
    
    def get_last_edit_log_by_live_video_id(self, live_video_id: uuid4) -> LiveVideoEditLogReadModel:
        return self.db.query(LiveVideoEditLog).filter(LiveVideoEditLog.live_video_id == live_video_id).order_by(LiveVideoEditLog.created_at.desc()).first()