from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: bool
    category_id: int

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True
