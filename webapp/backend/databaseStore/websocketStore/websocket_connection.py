

from typing import Annotated, Optional
from uuid import UUID

from fastapi import Depends

from sqlalchemy.orm import Session

from models.websocket_connections import WebSocketConenction, WebSocketCreateModel, WebSocketReadModel

from database import get_db


class WebSocketConnectionsResipository:

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db


    def create_cleint_conenction( self,  conection_data : WebSocketCreateModel ) -> WebSocketReadModel:
        webSocketConnection = WebSocketConenction(**conection_data.dict())

        self.db.add(webSocketConnection)
        self.db.commit()
        self.db.refresh(webSocketConnection)
        return webSocketConnection

    

    def delete_client_connection_by_client_id(self, client_id : UUID) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConenction).filter(WebSocketConenction.client_id == client_id).first()
        if not webSocketConnection:
            return None
        self.db.delete(webSocketConnection)
        self.db.commit()
        return webSocketConnection
    

    def  get_client_connection_by_client_id(self, client_id : UUID) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConenction).filter(WebSocketConenction.client_id == client_id).first()
        if not webSocketConnection:
            return None
        return webSocketConnection
    
    def get_client_connections_by_group_name(self, group_name : str) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConenction).filter(WebSocketConenction.group_name == group_name).all()
        if not webSocketConnection:
            return None
        return webSocketConnection
    
    
    