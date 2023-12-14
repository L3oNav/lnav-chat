from app.utils import Manager
from FASTAPI import UploadFile, File
from pydub import AudioSegment
from app.settings.rabbitmq import rabbitmq
import pika, json, uuid, io

class Audio(Manager):

    def __init__(self, sample_rate = 44100, segment_duration = 15000):
        self.sample_rate = sample_rate
        self.segment_duration = segment_duration
        self.queue = rabbitmq.queue_declare(queue="audio_processing")

    def new_audio(self, filename, audio_url):
        file = self.download_file(audio_url)
        audio = AudioSegment.from_file(file, format="wav")
        return self.split_and_upload(filename, audio, audio_url)
   
    def split_and_upload(self, filename, audio, audio_url):
        audio_duration = len(audio)
        if audio_duration <= block_duration:
            self.publish_to_queue(body={"audio_url": audio_url, "filename": filename})
        else:
            for i in range(0, audio_duration, self.segment_duration):
                audio_segment = audio[i:i+self.segment_duration]
                segment_name = f"{filename}-{str(uuid.uuidv4())}.wav"
                audio_segment.export(segment_name, format="wav")
                self.publish_to_queue(body={"audio_url": audio_url, "filename": segment_name})
    
    def publish_queue(self, body):
        rabbitmq.basic_publish(exchange="", routing_key="audio_processing", body=body)
