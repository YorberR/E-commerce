from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from crud import order as crud_order
from deps.deps import get_db, get_current_user

api_router = APIRouter()


def _serialize(order):
    return {
        "id": order.id,
        "date": order.date,
        "total_price": order.total_price,
        "details": [
            {
                "product_id": detail.product_id,
                "quantity": detail.quantity,
                "sub_total": detail.sub_total,
            }
            for detail in order.detail
        ],
    }


@api_router.get("/")
def list_orders(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return [_serialize(order) for order in crud_order.get_orders(db, user.id)]


@api_router.get("/{order_id}")
def get_order(order_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    order = crud_order.get_order(db, order_id, user.id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return _serialize(order)


@api_router.post("/checkout", status_code=status.HTTP_201_CREATED)
def checkout(db: Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        order = crud_order.create_order(db, user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return _serialize(order)
