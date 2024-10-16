
from websocket.websocket import ConnectionManager

connection_manager = None

def get_connection_manager() -> ConnectionManager:
    global connection_manager
    if connection_manager is None:
        connection_manager = ConnectionManager()
    return connection_manager