from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey, TIMESTAMP, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from db import Base
import uuid

USERS_ID = "users.id"

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_driver = Column(Boolean, default=False)
    vehicle_info = Column(JSON, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)
    updated_at = Column(TIMESTAMP, nullable=False)

class Ride(Base):
    __tablename__ = "rides"
    
    driver_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    driver_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    start_point = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    date_time = Column(TIMESTAMP, nullable=False)
    seats = Column(Integer, nullable=False)
    cost_per_seat = Column(Float, nullable=True)
    created_at = Column(TIMESTAMP, nullable=False)

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    passenger_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    ride_id = Column(UUID(as_uuid=True), ForeignKey("rides.id"))
    passenger_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    booked_at = Column(TIMESTAMP, nullable=False)

class Chat(Base):
    __tablename__ = "chat"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    sender_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    ride_id = Column(UUID(as_uuid=True), ForeignKey("rides.id"))
    sender_id = Column(UUID(as_uuid=True), ForeignKey(USERS_ID))
    message = Column(String, nullable=False)
    sent_at = Column(TIMESTAMP, nullable=False)