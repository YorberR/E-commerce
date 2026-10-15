from fastapi import APIRouter, Depends, HTTPException
from deps.deps import require_admin, get_db
from sqlalchemy.orm import Session
from fastapi import APIRouter
from schemas.product import ProductCreate
from crud.product import *

api_router = APIRouter()

@api_router.get("/products", response_model=list[ProductCreate])
def list_products(db: Session = Depends(get_db)):
    return get_products(db)
    

@api_router.post("/products", response_model=ProductCreate, dependencies=[Depends(require_admin)])
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, product)

@api_router.put("/products/{product_id}", response_model=ProductCreate, dependencies=[Depends(require_admin)])
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@api_router.delete("/products/{product_id}", response_model=ProductCreate, dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product