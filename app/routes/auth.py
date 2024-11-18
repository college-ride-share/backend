from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import user_schemas as schemas
from crud import user as crud
import db
import bcrypt
from lib.token import Token, authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, pwd_context
from datetime import datetime, timedelta, timezone

router = APIRouter()

# POST /signup - Create a new user
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    return crud.create_user(db, user)

# POST /login - Login a user
@router.post("/login")
async def login(user: schemas.UserLogin, db: Session = Depends(db.get_db)) -> Token:
    user = authenticate_user(db, user.email, user.password)
    # print(user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    # Map user to UserResponse
    user_response = schemas.UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        is_driver=user.is_driver
    )

    return Token(access_token=access_token, token_type="bearer", user=user_response)
