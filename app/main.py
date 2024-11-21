import uvicorn
from typing import Union
from fastapi import FastAPI

from routes import auth, rides, bookings, chat
from db import Base, engine
import redis
from utils.redis_helper import redis_client



# Initialize FastAPI app
app = FastAPI(
    title="Campus Ride-Sharing API",
    description="API for a campus ride-sharing app built with FastAPI and PostgreSQL.",
    version="1.0.0",
)



# Include routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(rides.router, prefix="/rides", tags=["Rides"])
# app.include_router(bookings.router, prefix="/bookings", tags=["Bookings"])
# app.include_router(chat.router, prefix="/chat", tags=["Chat"])


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)