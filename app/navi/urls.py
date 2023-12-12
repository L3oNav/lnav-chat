from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from app.navi.sockets import WSMessages()

router = APIRouter(prefix="/v1/auth")

messenger = WSMessages()

@app.websocket("/ws/{client_id}")
async def messenger_endpoint(websocket: WebSocket):
    await messenger.connect(websocket)
    try: 
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{client_id} has left the chat")
