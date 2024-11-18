from sqlalchemy.orm import Session
import models

from schemas import user_schemas as schemas

# CRUD operations for users
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

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()
