from sqlalchemy.orm import Session
from . import models, schemas

# CRUD operations for rides
def create_ride(db: Session, ride: schemas.RideCreate):
    db_ride = models.Ride(**ride.dict())
    db.add(db_ride)
    db.commit()
    db.refresh(db_ride)
    return db_ride

def get_ride(db: Session, ride_id: str):
    return db.query(models.Ride).filter(models.Ride.id == ride_id).first()