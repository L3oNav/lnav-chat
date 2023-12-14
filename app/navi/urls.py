from fastapi import APIRouter, Depends, HTTPException, Response, Cookie, status
from app.navi.manager import navi_manager
router_chat = APIRouter(prefix="/v1/chat")

@router_chat.websocket("/ws/{client_id}")
async def messenger_endpoint(websocket: WebSocket):
    await websocket.accept()
    user = request.session['key']
    websocket_connection[user] = websocket
    try: 
        while True:
            if mesaage_type == 'text':
                message_text = await websocket.receive_text()
                message_data = json.loads(message_text)
                message_type = message_data['type']
                for _user, user_ws in websocket_connection.items():
                    if _user != message_data['sender']:
                    await user_ws.send_text(f"message: {message_data['message']}")

            if message_type == 'audio/wav':
                audio_file = await websocket.receive_bytes()
                navi_manager.new_audio_message(
                    sender=user, receiver=message_data['receiver'], audio_file=audio_file
                )
                await websocket_connection[message_data['receiver']].send_text(message_text)

            if message_type == 'file':
                file = await websocket.receive_bytes()
                navi_manager.new_file_message(
                    sender=user, receiver=message_data['receiver'], file=file
                )
                await websocket_connection[message_data['receiver']].send_text(message_text)

            await websocket.send_personal_message(f"You wrote: {data}", websocket)
            await websocket.broadcast(f"Client #{client_id} says: {data}")
    except WebSocketDisconnect:

