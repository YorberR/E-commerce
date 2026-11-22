from datetime import datetime

from pydantic import BaseModel


class OrderDetailResponse(BaseModel):
    product_id: int
    quantity: int
    sub_total: float


class OrderResponse(BaseModel):
    id: int
    date: datetime
    total_price: float
    details: list[OrderDetailResponse]
