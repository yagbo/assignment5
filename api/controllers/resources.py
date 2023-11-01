from fastapi import Response, status
from sqlalchemy.orm import Session
from ..models import models, schemas

def create(db: Session, resource):
    db_resource = models.Resource(name=resource.name, quantity=resource.quantity)
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource

def read_all(db: Session):
    return db.query(models.Resource).all()

def read_one(db: Session, resource_id):
    return db.query(models.Resource).filter(models.Resource.id == resource_id).first()

def update(db: Session, resource_id, resource):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    for key, value in resource.dict(exclude_unset=True).items():
        setattr(db_resource, key, value)

    db.commit()
    return db_resource

def delete(db: Session, resource_id):
    db_resource = db.query(models.Resource).filter(models.Resource.id == resource_id).first()
    if db_resource is None:
        return Response(status_code=status.HTTP_404_NOT_FOUND)

    db.delete(db_resource)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
