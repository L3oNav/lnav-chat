from app.settings.rabbitmq import rabbitmq
import pika, json
import uuid

class Audio():
    

    def __init__(self, sample_rate = 44100, segment_duration = 10):
        self.audio_bytes = b""
        self.sample_rate = sample_rate
        self.segment_duration = segment_duration

    def receive_audio(self, audio_bytes):
        self.audio_bytes += audio_bytes

    def split_audio(self):
        segments = []
        segment_duration_samples = int(segment_duration * sample_rate)
        num_segments = int(len(audio) / segment_duration_samples)
        for i in range(num_segments):
            start_sample  = i * segment_duration_samples
            end_sample    = start_sample + segment_duration_samples
            segment_audio = audio[start_sample:end_sample]
            segments.append(segment_audio)
        return segments

    def save_segments(self):
        audio_segments = self.split_audio()
        segment_filenames = []
        for i, segment_audio in enumerate(audio_segments):
            filename = f"{str(uuid.uuid4())}.wav"
            # TODO: upload to s3
            self.save_wav(filename, segment_audio)
            segment_filenames.append(filename)
        return segment_filenames

    def save_wav(self, filename, audio):
        wave_data = audio.to_buffer()
        with wave_data.open(filename, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframe_rate(self.sample_rate)
            wf.writeframes(wave_data)
        message = {
            "user_id": f"3bc34bdb-4538-43dd-86ea-c4132b58939d",
            "filename": filename
        }
        rabbitmq.basic_publish(
            exchange="",
            routing_key="audio",
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
            )
        )
