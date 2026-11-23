from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from crud import product as crud_product
from deps.deps import get_db, require_admin
from schemas.product import ProductCreate, ProductResponse

api_router = APIRouter()


@api_router.get("/", response_model=list[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return crud_product.get_products(db)


@api_router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_admin)],
)
def add_product(product: ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db, product)


@api_router.put("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_admin)])
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db)):
    product = crud_product.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@api_router.delete("/{product_id}", response_model=ProductResponse, dependencies=[Depends(require_admin)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud_product.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
