from fastapi import UploadFile, File, HTTPException
from app.settings.object_storage import upload_file_to_bucket
import uuid

class Manager:

    def __init__(self, session):
        self.KB = 1024
        self.MB = 1024 * self.KB
        self.MAX_SIZE = 25 * self.MB
        self.permited_formats = ['png', 'jpg', 'jpeg', 'pdf', 'wav']
        self.redis = None
        self.session = None

    async def upload_audio(self, file: UploadFile = File(...)):
        try:
            if self.MAX_SIZE < (file.size * self.MB):
                return False
            file_name = f"{str(uuid.uuid4())}.wav"
            file_obj = file.file
            response = upload_file_to_bucket(file_obj, object_name=file_name)
            return response
        except Exception as e:
            print(e)
            return False

    async def upload_file(self, file: UploadFile = File(...)):
        try:
            file_name = file.filename
            file_obj = file.file
            if file_name.split('.')[-1] not in self.permited_formats:
                raise HTTPException(status_code=400, detail="File format not permited")
            response = upload_file_to_bucket(file_obj, object_name=file_name)
            return response
        except Exception as e:
            print(e)
            return False

