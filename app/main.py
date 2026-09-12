from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas


app = FastAPI()

@app.get("/products", response_model=list[schemas.ProductCreate])
def get_products(db: Session = Depends(get_db)):
    return crud.get_products(db)
    

@app.post("/products", response_model=schemas.ProductCreate)
def add_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db, product)

@app.put("/products/{product_id}", response_model=schemas.ProductCreate)
def update_product(product_id: int, data: schemas.ProductCreate, db: Session = Depends(get_db)):
    product = crud.update_product(db, product_id, data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.delete("/products/{product_id}", response_model=schemas.ProductCreate)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product