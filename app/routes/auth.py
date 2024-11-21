from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import user_schemas as schemas 
from crud import user as crud
import db
import bcrypt
from utils.token import (
    Token,
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
)
from datetime import datetime, timedelta, timezone
import random
import string
from utils.redis_helper import redis_client
from utils.password_validator import validate_password


router = APIRouter()

# POST /signup - Create a new user
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    if not validate_password(user.password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 8 characters long, contain at least one uppercase letter, "
                "one lowercase letter, one number, and one special character."
            ),
    )
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
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access and refresh tokens
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": user.email})
    
    # Map user to UserResponse
    user_response = schemas.UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        is_driver=user.is_driver
    )

    return Token(access_token=access_token, token_type="bearer", user=user_response, refresh_token=refresh_token)

# POST /refresh - Refresh an access token
@router.post("/refresh")
async def refresh_token(refresh_token: str, db: Session = Depends(db.get_db)) -> Token:
    # Verify refresh token
    token_data = verify_refresh_token(refresh_token)
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from email in the token data
    user = crud.get_user_by_email(db, token_data["sub"])
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Create a new access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    refresh_token = create_refresh_token(data={"sub": user.email})


    # Map user to UserResponse
    user_response = schemas.UserResponse(
        id=str(user.id),
        email=user.email,
        name=user.name,
        is_driver=user.is_driver
    )

    return Token(access_token=access_token, token_type="bearer", user=user_response, refresh_token=refresh_token)

# POST /check-email - Check if email is already registered
@router.post("/check-email")
def check_email(email: schemas.Email, db: Session = Depends(db.get_db)):
    existing_user = crud.get_user_by_email(db, email.email)
    if existing_user:
        return {"registered": True}
    return {"registered": False}

# POST /request-reset - Request a password reset
@router.post("/request-reset")
def request_reset(email: schemas.Email, db: Session = Depends(db.get_db)):
    user = crud.get_user_by_email(db, email.email)
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Generate a reset token
    reset_token = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    # Store the reset token in Redis
    redis_client.setex(f"reset_code:{email.email}", 600, reset_token)
    
    # TODO: Send an email with the reset token
    # send_email(
    #     email=email.email,
    #     subject="CarShareU Password Reset",
    #     message=f"Use this token to reset your password: {reset_token}",
    # )
    print(f"Reset token: {reset_token}")
    
    return {"message": "Password reset token sent to email"}

# POST /verify-reset - Verify a password reset token
@router.post("/verify-reset")
def verify_reset(reset: schemas.VerifyResetCode):
    reset_token = redis_client.get(f"reset_code:{reset.email}")
    if not reset_token:
        raise HTTPException(status_code=400, detail="Reset token expired or invalid")
    
    if reset_token != reset.code:
        raise HTTPException(status_code=400, detail="Invalid reset token")
    
    return {"valid": True}

# POST /reset-password - Reset user password
@router.post("/reset-password")
def reset_password(reset: schemas.ResetPassword, db: Session = Depends(db.get_db)):
    if reset.new_password != reset.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")
    
    if not validate_password(reset.new_password):
        raise HTTPException(
            status_code=400,
            detail=(
                "Password must be at least 8 characters long, contain at least one uppercase letter, "
                "one lowercase letter, one number, and one special character."
            ),
        )
    
    user = crud.get_user_by_email(db, reset.email)

    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Hash the new password
    hashed_password = pwd_context.hash(reset.new_password)
    
    # Update the user's password
    crud.reset_password(db, reset.email, hashed_password)
    
    return {"message": "Password reset successful"}