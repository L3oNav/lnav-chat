from app.audio import Audio
from fastapi.testclient import TestClient
#from app.main import app
import unittest
import weve

def test_audio_handler():
    with wave.open('Test.wav', mode='rb') as f:
        #audio = Audio()
        #audio.receive_audio(f)
        print(f)
    assert True
