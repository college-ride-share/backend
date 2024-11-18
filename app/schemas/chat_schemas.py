from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Chat schemas
class ChatMessageCreate(BaseModel):
    ride_id: str
    sender_id: str
    message: str

class ChatMessageResponse(ChatMessageCreate):
    id: str
    sent_at: datetime

    class Config:
        orm_mode = True