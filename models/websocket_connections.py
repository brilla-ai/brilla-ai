from typing import Optional

from pydantic import BaseModel

from sqlalchemy import Column, Integer, String

from database import Base

from BaseModel import DefaultData

#  TODO:  Implement the persistence of the connection ids later 
class WebSocketConenction(Base , DefaultData):
    __tablename__ = "websocket_connections"
    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(String, index=True)
    group_name = Column(String)


class WebSocketReadModel(BaseModel):
    client_id: str
    group_name: str

    class Config:
        from_attributes = True


class WebSocketUpdateModel(BaseModel):
    client_id: Optional[str] = None
    group_name: Optional[str] = None

    class Config:
        from_attributes = True


class WebSocketCreateModel(BaseModel):
    client_id: str
    group_name: Optional[str] = None

    class Config:
        from_attributes = True


class WebSocketDeleteModel(BaseModel):
    client_id: str
    group_name: Optional[str] = None

    class Config:
        from_attributes = True



