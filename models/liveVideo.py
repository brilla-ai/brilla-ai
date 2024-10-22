from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from uuid import uuid4
from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Boolean, Column, DateTime, ForeignKey, String, func, event,  Enum as SqlAlchemyEnum
from sqlalchemy.orm import relationship
from .BaseModel import DefaultData
from database import Base
from uuid import UUID as type_uuid


#  Enum 
class  VideoStatus (Enum):
    live = "live"
    ended = "ended"
    upcoming = "upcoming"
    draft = "draft"


# Entity

class LiveVideo(Base, DefaultData):
    __tablename__ = "live_video"
    video_link = Column(String, nullable= False)
    schedule = Column(Boolean , default=False)
    tag = Column(String, nullable= False)
    start_time = Column(DateTime, default=None , nullable=True)
    end_time = Column(DateTime, default=None, nullable=True)
    status =  Column(SqlAlchemyEnum(VideoStatus), default=VideoStatus.upcoming)
    edit_log = relationship("LiveVideoEditLog", back_populates="live_video")
    stop_time = Column(DateTime, default=None, nullable=True)


# Automatic status update logic
def set_live_video_status(mapper, connection, target):
    """
    Event listener to automatically set status before insert or update.
    """
    # Make 'now' timezone-aware using UTC
    now = datetime.now(timezone.utc)

    # Ensure 'target.start_time' and 'target.end_time' are timezone-aware (UTC)
    if target.start_time and target.start_time.tzinfo is None:
        target.start_time = target.start_time.replace(tzinfo=timezone.utc)
    
    if target.end_time and target.end_time.tzinfo is None:
        target.end_time = target.end_time.replace(tzinfo=timezone.utc)

    # If both start_time and end_time are None or in the past, set status to "draft"
    if (not target.start_time and not target.end_time) or (
        target.start_time and target.start_time < now and 
        target.end_time and target.end_time < now
    ):
        target.status = "draft"
    else:
        target.status = "upcoming"

# Validator function for start_time and end_time
def validate_start_and_end_time(mapper, connection, target):
    """Ensure that start_time is less than end_time."""
    if target.start_time and target.end_time and target.start_time > target.end_time:
        raise ValueError("start_time cannot be greater than end_time")

# Listen for the 'before_insert' and 'before_update' events
event.listen(LiveVideo, 'before_insert', validate_start_and_end_time)
event.listen(LiveVideo, 'before_update', validate_start_and_end_time)

# Listen for the 'before_insert' and 'before_update' events
event.listen(LiveVideo, 'before_insert', set_live_video_status)
event.listen(LiveVideo, 'before_update', set_live_video_status)




class LiveVideoEditLog(Base, DefaultData):
    __tablename__ = "live_video_edit_log"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid4)
    live_video_id = Column(UUID(as_uuid=True), ForeignKey("live_video.id", ondelete="CASCADE"))
    live_video = relationship("LiveVideo", back_populates="edit_log")
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    user = relationship("User")



#  Pydantic models 

class LiveVideoReadModel(BaseModel):
    id: type_uuid
    video_link: str
    schedule: bool
    tag: str
    start_time: Optional[datetime]  = None 
    end_time: Optional[datetime]  = None 
    status: VideoStatus
    stop_time: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

    # class Config: 
    #     orm_mode = True


class LiveVideoCreateModel(BaseModel):
    video_link: str
    schedule: bool
    tag: str
    start_time: Optional[datetime]  = None
    end_time: Optional[datetime]
    status: Optional[VideoStatus] = VideoStatus.live

    


class LiveVideoUpdateModel(BaseModel):
    id: type_uuid
    video_link: Optional[str] = None
    schedule: Optional[bool] = None
    tag: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[VideoStatus] = None


class LiveVideoUpdateStopStatusModel(BaseModel):
    id: type_uuid
    stop : bool 

class LiveVideoEditLogReadModel(BaseModel):
    id: type_uuid
    user_id: type_uuid
    live_video_id: type_uuid
    created_at: datetime

    class Config: 
        from_attributes = True


class  LiveVideoEditLogCreateModel(BaseModel):
    user_id: type_uuid
    live_video_id: type_uuid
    updated_at: datetime



class  LiveVideoEditLogUpdateModel(BaseModel):
    id: type_uuid
    user_id: Optional[type_uuid] = None
    live_video_id: Optional[type_uuid] = None
    updated_at: Optional[datetime] = None