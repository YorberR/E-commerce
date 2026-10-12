from fastapi import APIRouter, Depends, HTTPException
from deps.deps import require_admin, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter
import crud, schemas

api_router = APIRouter()

@api_router.get("/products", response_model=list[schemas.ProductCreate])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)
    

@api_router.post("/products", response_model=schemas.ProductCreate, dependencies=[Depends(require_admin)])
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@api_router.put("/products/{product_id}", response_model=schemas.ProductCreate, dependencies=[Depends(require_admin)])
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api_router.delete("/products/{product_id}", response_model=schemas.ProductCreate, dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product