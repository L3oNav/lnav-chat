
from pydantic import BaseModel, Field, validator

class NewMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)
    user_id: int = Field(..., gt=0)
    recipient_id: int = Field(..., gt=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @validator('message')
    def message_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Must not be empty')
        return v
