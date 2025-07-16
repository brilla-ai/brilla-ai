from typing import Annotated, Optional

from uuid import UUID

from fastapi import Depends

from sqlalchemy.orm import Session

from models.websocket_connections import WebSocketConnection, WebSocketCreateModel, WebSocketReadModel

from database import get_db


class WebSocketConnectionsRepository:

    def __init__(self, db: Annotated[Session, Depends(get_db)]):
        self.db = db


    def create_client_connection( self,  connection_data : WebSocketCreateModel ) -> WebSocketReadModel:
        webSocketConnection = WebSocketConnection(**connection_data.dict())

        self.db.add(webSocketConnection)
        self.db.commit()
        self.db.refresh(webSocketConnection)
        return webSocketConnection

    

    def delete_client_connection_by_client_id(self, client_id : UUID) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConnection).filter(WebSocketConnection.client_id == client_id).first()
        if not webSocketConnection:
            return None
        self.db.delete(webSocketConnection)
        self.db.commit()
        return webSocketConnection
    

    def  get_client_connection_by_client_id(self, client_id : UUID) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConnection).filter(WebSocketConnection.client_id == client_id).first()
        if not webSocketConnection:
            return None
        return webSocketConnection
    
    def get_client_connections_by_group_name(self, group_name : str) -> Optional[WebSocketReadModel]:
        webSocketConnection = self.db.query(WebSocketConnection).filter(WebSocketConnection.group_name == group_name).all()
        if not webSocketConnection:
            return None
        return webSocketConnection
    
    
    