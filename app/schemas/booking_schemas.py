from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookingCreate(BaseModel):
    ride_id: str
    passenger_id: str

class BookingResponse(BookingCreate):
    id: str
    booked_at: datetime

    class Config:
        orm_mode = True