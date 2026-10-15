from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps.deps import require_admin, get_db
from fastapi import APIRouter
from schemas.category import CategoryCreate
from crud.category import get_categories, create_category, update_category, delete_category

api_router = APIRouter()

@api_router.get("/categories", response_model=list[CategoryCreate])
def list_categories(db: Session = Depends(get_db)):
    return get_categories(db)

@api_router.post("/categories", response_model=CategoryCreate, dependencies=[Depends(require_admin)])
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return create_category(db, category)

@api_router.put("/categories/{category_id}", response_model=CategoryCreate, dependencies=[Depends(require_admin)])
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@api_router.delete("/categories/{category_id}", response_model=CategoryCreate, dependencies=[Depends(require_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = delete_category(db, category_id)
    if not category:    
        raise HTTPException(status_code=404, detail="Category not found")
    return category