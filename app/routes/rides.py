from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import db
from schemas import ride_schemas as schemas
import models

# Create a router
router = APIRouter()

# POST /rides - Create a new ride
@router.post("")
def create_ride(ride: schemas.RideCreate, db: Session = Depends(db.get_db)):
    new_ride = models.Ride(**ride.dict())
    db.add(new_ride)
    db.commit()
    db.refresh(new_ride)
    return new_ride