import shutil
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from schemas import user_schemas as schemas 
from sqlalchemy.orm import Session
from crud import user as crud
import db


router = APIRouter()

# GET /user/{user_id} - Get a user by ID
@router.get("/{user_id}")
async def get_user_by_id(user_id: str, db: Session = Depends(db.get_db)) -> schemas.UserResponse:
    print(f"Getting user with ID: {user_id}")
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

# POST /user/{user_id}/upload-photo - Upload a profile picture

@router.post("/{user_id}/upload-photo")
async def upload_photo(user_id: str, file: UploadFile = File(...), db: Session = Depends(db.get_db)):
    print(f"Uploading photo for user with ID: {user_id}")

    # Validate user
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Save the file (example: store locally)
    try:
        with open(f"uploads/{user_id}_{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        print(f"Failed to save file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Return response
    return {
        "id": str(user.id),
        "email": user.email,
        "firstname": user.firstname,
        "lastname": user.lastname,
        "dob": user.dob,
        "message": "File uploaded successfully"
    }
