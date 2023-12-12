from app.users.models import User
from app.settings.database import get_session as db_session
from app.settings import get_settings
from fastapi import Depends, Request, HTTPException, Security, UploadFile, File,status
from datetime import datetime, timedelta
from typing import Annotated
from pydantic import ValidationError
from jose import jwt
from app.utils.manager import Manager
from app.settings.redis import get_redis_connection
from app.settings.object_storage import upload_file_to_bucket
from sqlalchemy import or_
import asyncio
import json

class MessagerManager(Manager):
   
    def __init__(self):
        self.session = db_session()
        self.redis = get_redis_connection()

    async def get_user_by_id(self, user_id):
        user = await self.session.query(User).filter(User.id == user_id).first()
        return user

    async def get_user_by_email(self, email):
        user = await self.session.query(User).filter(User.email == email).first()
        return user
    
    async def get_messages(self, user_id):
        try:
            messages = await self.session.query(Message).filter(
                or_(Message.sender_id == user_id, Message.receiver_id == user_id)
            ).limit(100).all()
            return messages
        except Exception as e:
            print(e)
            return False

    async def new_message(self, sender_id, receiver_id, message):
        try:
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                message=message
            )
            self.session.add(new_message)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    async def new_audio_message(self, sender_id, receiver_id, audio_file: UploadFile = File(...)):
        try:
            response = self.upload_audio(audio_file)
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                attachment=True,
                attachment_url=response['public_url']
            )
            self.session.add(new_message)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

    async def new_file_message(self, sender_id, receiver_id, file: UploadFile = File(...)):
        try:
            response = self.upload_file(file)
            new_message = Message(
                sender_id=sender_id,
                receiver_id=receiver_id,
                attachment=True,
                attachment_url=response['public_url']
            )
            self.session.add(new_message)
            self.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
