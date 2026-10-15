from core.security import verify_password, create_access_token
from fastapi import APIRouter, Depends, HTTPException, status
from deps.deps import get_current_user, require_admin, get_db
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.user import UserCreate
from schemas.token import Token
from crud.user import *

api_router = APIRouter()

@api_router.get("/users", response_model=UserCreate, status_code=status.HTTP_200_OK)
def list_users(db: Session = Depends(get_db)):
    return get_user(db)

@api_router.post("/users", response_model=UserCreate, status_code=status.HTTP_201_CREATED, dependencies=[Depends(require_admin)])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        return create_user(db, user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@api_router.post("/login", response_model=Token, status_code=status.HTTP_200_OK)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = get_user_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@api_router.get("/users/me", response_model=UserCreate, status_code=status.HTTP_200_OK)
def read_users_me(current_user = Depends(get_current_user)):    
    return current_user