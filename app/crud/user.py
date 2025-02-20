from sqlalchemy.orm import Session
import models
from datetime import datetime
from schemas import user_schemas as schemas
import uuid

# CRUD operations for users

# Create user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, 
        password=user.password,
        firstname=user.firstname,
        lastname=user.lastname,
        dob=datetime.strptime(user.dob, "%m/%d/%y"),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Get user by ID
def get_user_by_id(db: Session, user_id: str):
    user = db.query(models.User).filter(models.User.id == uuid.UUID(user_id).hex).first()
    if user:
        user.id = str(user.id)  # Convert UUID to string
    return user

# Reset password
def reset_password(db: Session, email: str, new_password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user