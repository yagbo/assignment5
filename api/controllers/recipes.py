# recipes.py
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import models, schemas

def read_one(db: Session, recipe_id):
    return db.query(models.Recipe).get(recipe_id)

def create_recipe(db: Session, recipe: schemas.RecipeCreate):
    db_recipe = models.Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def get_recipes(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Recipe).offset(skip).limit(limit).all()

def get_recipe(db: Session, recipe_id: int):
    recipe = db.query(models.Recipe).get(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    return recipe

def update_recipe(db: Session, recipe_id: int, recipe: schemas.ResourceUpdate):
    db_recipe = db.query(models.Recipe).get(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")

    # Update model from dict and skip non-set (None) fields
    for key, value in recipe.dict(exclude_unset=True).items():
        setattr(db_recipe, key, value)

    db.commit()
    db.refresh(db_recipe)
    return db_recipe

def delete_recipe(db: Session, recipe_id: int):
    db_recipe = db.query(models.Recipe).get(recipe_id)
    if db_recipe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return {"detail": "Recipe deleted"}
