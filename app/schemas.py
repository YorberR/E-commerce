from pydantic import BaseModel, EmailStr

class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: bool
    category_id: int

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True

class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryCreate):
    id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str
    is_admin: bool = False

class UserResponse(UserBase):
    id: int
    is_admin: bool

    class Config:
        orm_mode = True