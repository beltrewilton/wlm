from fastapi import WebSocket, WebSocketDisconnect
from typing import List
import asyncio
from aiocache import Cache


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket, client_uuid: str, myvar: Cache):
        await websocket.accept()
        self.active_connections.append(websocket)
        client_uuid_list = await myvar.get('client_uuid_list')
        client_uuid_list.append(client_uuid)
        await myvar.set('client_uuid_list', client_uuid_list)

    async def disconnect(self, websocket: WebSocket, client_uuid: str, myvar: Cache):
        self.active_connections.remove(websocket)
        sharable_per_client = await myvar.get('sharable_per_client')
        # remove...
        sharable_per_client_copy = [value for value in sharable_per_client if value['client_uuid'] != client_uuid]
        await myvar.set('sharable_per_client', sharable_per_client_copy)
        print(f'Client: {client_uuid} left ...')

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_json(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


async def send_periodically(websocket, manager, client_uuid,  timer, myvar):
    try:
        while True:
            sharable_per_client = await myvar.get('sharable_per_client')
            sharable = [value for value in sharable_per_client if value['client_uuid'] == client_uuid]
            if len(sharable) > 0:    # some info for sent to client_uuid ?
                await manager.send_personal_message(sharable[0], websocket)
                # purge sharable client_uuid recently sent.
                sharable_per_client_copy = [value for value in sharable_per_client if value['client_uuid'] != client_uuid]
                await myvar.set('sharable_per_client', sharable_per_client_copy)
            await asyncio.sleep(timer)
    except WebSocketDisconnect:
        await manager.disconnect(websocket, client_uuid)
        # await manager.broadcast(f"Client #{client_uuid} left the chat")