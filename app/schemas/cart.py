from pydantic import BaseModel


class CartItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    sub_total: float


class CartResponse(BaseModel):
    id: int
    user_id: int
    total_price: float
    items: list[CartItemResponse]


class CartAddResponse(BaseModel):
    message: str
    item: CartItemResponse


class MessageResponse(BaseModel):
    message: str
