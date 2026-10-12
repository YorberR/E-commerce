from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps.deps import require_admin, get_db
from fastapi import APIRouter
import crud, schemas

api_router = APIRouter()

@api_router.get("/categories", response_model=list[schemas.CategoryCreate])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@api_router.post("/categories", response_model=schemas.CategoryCreate, dependencies=[Depends(require_admin)])
def add_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@api_router.put("/categories/{category_id}", response_model=schemas.CategoryCreate, dependencies=[Depends(require_admin)])
def update_category(category_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = crud.update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@api_router.delete("/categories/{category_id}", response_model=schemas.CategoryCreate, dependencies=[Depends(require_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.delete_category(db, category_id)
    if not category:    
        raise HTTPException(status_code=404, detail="Category not found")
    return category