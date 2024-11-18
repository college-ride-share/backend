from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from schemas import user_schemas as schemas
from crud import user as crud
import db
import bcrypt

router = APIRouter()



# POST /signup - Create a new user
@router.post("/signup")
def signup(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    existing_user = crud.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    user.password = hashed_password
    return crud.create_user(db, user)

# POST /login - Login user
# @router.post("/login")
# def login(user: schemas.UserLogin, db: Session = Depends(database.get_db)):
#     user_db = db.query(models.User).filter(models.User.email == user.email).first()
#     if not user_db:
#         return {"error": "Invalid credentials"}
#     if not bcrypt.checkpw(user.password.encode('utf-8'), user_db.password.encode('utf-8')):
#         return {"error": "Invalid credentials"}
#     return user_db
