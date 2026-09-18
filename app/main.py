from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
import crud, schemas
from fastapi.security import OAuth2PasswordRequestForm
from depends import get_current_user, require_admin


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

##### User #####

@app.get("/users", response_model=schemas.UserCreate, status_code=status.HTTP_200_OK)
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@app.post("/users", response_model=schemas.UserCreate, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@app.post("/login", response_model=schemas.Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=schemas.UserCreate, status_code=status.HTTP_200_OK)
def read_users_me(current_user = Depends(get_current_user)):    
    return current_user