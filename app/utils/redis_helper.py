from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session
from db import get_db
from models import User

import redis

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)