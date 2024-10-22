



from typing import Annotated
from fastapi import APIRouter, Depends, WebSocket

from services.websocketService.websocket import WebSocketService
from core.command_handler.factory import get_command_handler
from websocket.websocket_command_handler import CommandHandler


websocket_router  =  APIRouter(tags=["websocket"], prefix="/websocket")


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket : WebSocket, websocket_service : Annotated[WebSocketService, Depends(WebSocketService)], command_handler: Annotated[CommandHandler, Depends(get_command_handler)] ):
    await websocket_service.connect(websocket)
    await  websocket_service.on_message_recieved_handler(websocket, command_handler)
    