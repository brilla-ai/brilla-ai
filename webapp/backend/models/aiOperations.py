from typing import Optional
from uuid import uuid4,  UUID as type_uuid 

from pydantic import BaseModel, ConfigDict
from sqlalchemy import UUID, Boolean, Column, Enum as SqlAlchemyEnum

from database import Base

from enum import Enum

from .BaseModel import DefaultData




class Rounds ( Enum):
    STAGE1 =  "STAGE1"
    STAGE2 =  "STAGE2"
    STAGE3 =  "STAGE3"
    STAGE4 =  "STAGE4"
    STAGE5 =  "STAGE5"

class AIOperations(Base, DefaultData):
    __tablename__ = "ai_operations"
    stage_round =  Column( SqlAlchemyEnum(Rounds), default=Rounds.STAGE1)
    start_audio_processing = Column(Boolean, default=False)


#  Pydantic models
class  AIOperationsReadModel(BaseModel):
    id : type_uuid 
    stage_round: Rounds
    start_audio_processing: bool

    model_config = ConfigDict(from_attributes=True)



class AIOperationsUpdateModel(BaseModel):
    stage_round: Optional[Rounds] = None
    start_audio_processing: Optional[bool] = None

    class Config: 
        from_attributes = True



class VideoUrl(BaseModel):
    video_url: str