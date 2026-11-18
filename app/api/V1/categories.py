from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps.deps import require_admin, get_db
from schemas.category import CategoryCreate, CategoryResponse
from crud import category as crud_category

api_router = APIRouter()


@api_router.get("/", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)):
    return crud_category.get_categories(db)


@api_router.post("/", response_model=CategoryResponse, dependencies=[Depends(require_admin)])
def add_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return crud_category.create_category(db, category)


@api_router.put("/{category_id}", response_model=CategoryResponse, dependencies=[Depends(require_admin)])
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db)):
    category = crud_category.update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


@api_router.delete("/{category_id}", response_model=CategoryResponse, dependencies=[Depends(require_admin)])
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud_category.delete_category(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
