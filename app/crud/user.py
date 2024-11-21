from sqlalchemy.orm import Session
import models

from schemas import user_schemas as schemas

# CRUD operations for users

# Create user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email, 
        name=user.name, 
        password=user.password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# Reset password
def reset_password(db: Session, email: str, new_password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    user.password = new_password
    db.commit()
    db.refresh(user)
    return user