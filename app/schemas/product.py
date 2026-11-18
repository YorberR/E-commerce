from pydantic import BaseModel, ConfigDict

class ProductCreate(BaseModel):
    name: str
    price: float
    in_stock: bool = True
    stock: int = 0
    category_id: int

class ProductResponse(ProductCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
