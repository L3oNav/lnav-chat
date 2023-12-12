from fastapi import APIRouter, UploadFile
from typing import Optional, Annotation
from app.audio import Audio
import time

router = APIRouter(prefix="/v1/talk")

@router.post("/audio")
def audio_message(request):
    audio = Audio()
    audio.receive_audio(request.body)
    return {"status": "ok"}
    
