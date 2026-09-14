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

##### Category #####

@app.get("/categories", response_model=list[schemas.CategoryCreate])
def get_categories(db: Session = Depends(get_db)):
    return crud.get_categories(db)

@app.post("/categories", response_model=schemas.CategoryCreate)
def add_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    return crud.create_category(db, category)

@app.put("/categories/{category_id}", response_model=schemas.CategoryCreate)
def update_category(category_id: int, data: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category = crud.update_category(db, category_id, data)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@app.delete("/categories/{category_id}", response_model=schemas.CategoryCreate)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = crud.delete_category(db, category_id)
    if not category:    
        raise HTTPException(status_code=404, detail="Category not found")
    return category