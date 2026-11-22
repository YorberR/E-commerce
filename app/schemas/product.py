from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=5000)
    in_stock: bool = True
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(gt=0)


class ProductCreate(ProductBase):
    price: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class ProductResponse(ProductBase):
    id: int
    price: float

    model_config = ConfigDict(from_attributes=True)
