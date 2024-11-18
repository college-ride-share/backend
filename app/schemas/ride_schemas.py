from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# Ride schemas
class RideCreate(BaseModel):
    driver_id: str
    start_point: str
    destination: str
    date_time: datetime
    seats: int
    cost_per_seat: Optional[float] = None

class RideResponse(RideCreate):
    id: str

    class Config:
        orm_mode = True