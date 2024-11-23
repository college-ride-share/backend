from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    firstname: str
    lastname: str
    dob: str
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    email: EmailStr
    is_driver: bool
    firstname: str
    lastname: str
    dob: datetime

    class Config:
        orm_mode = True

class Email(BaseModel):
    email: EmailStr

class RequestResetCode(BaseModel):
    email: EmailStr

class VerifyResetCode(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)

class ResetPassword(BaseModel):
    email: EmailStr
    code: str = Field(min_length=6, max_length=6)
    new_password: str = Field(min_length=8)
    confirm_password: str = Field(min_length=8)