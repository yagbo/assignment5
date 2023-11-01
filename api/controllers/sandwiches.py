from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import models, schemas

def create_sandwich(db: Session, sandwich: schemas.SandwichCreate):
    db_sandwich = models.Sandwich(**sandwich.dict())
    db.add(db_sandwich)
    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def get_sandwiches(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Sandwich).offset(skip).limit(limit).all()

def get_sandwich(db: Session, sandwich_id: int):
    sandwich = db.query(models.Sandwich).get(sandwich_id)
    if sandwich is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    return sandwich

def update_sandwich(db: Session, sandwich_id: int, sandwich: schemas.SandwichUpdate):
    db_sandwich = db.query(models.Sandwich).get(sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")

    for key, value in sandwich.dict(exclude_unset=True).items():
        setattr(db_sandwich, key, value)

    db.commit()
    db.refresh(db_sandwich)
    return db_sandwich

def delete_sandwich(db: Session, sandwich_id: int):
    db_sandwich = db.query(models.Sandwich).get(sandwich_id)
    if db_sandwich is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sandwich not found")
    db.delete(db_sandwich)
    db.commit()
    return {"detail": "Sandwich deleted"}

def read_one(db: Session, sandwich_id):
    return db.query(models.Sandwich).get(sandwich_id)
