from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import cart as crud_cart
from deps.deps import get_db, get_current_user

api_router = APIRouter()


def _serialize_item(item):
    return {
        "id": item.id,
        "product_id": item.product_id,
        "quantity": item.quantity,
    }


def _serialize_cart(cart):
    items = []
    for item in cart.items:
        unit_price = item.product.price if item.product and item.product.price else 0.0
        items.append({
            **_serialize_item(item),
            "unit_price": unit_price,
            "sub_total": unit_price * item.quantity,
        })
    return {
        "id": cart.id,
        "user_id": cart.user_id,
        "total_price": cart.total_price,
        "items": items,
    }


@api_router.get("/", summary="view cart contents")
def view_cart(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return _serialize_cart(crud_cart.get_cart(db, user.id))


@api_router.post("/add/{product_id}")
def add_product(product_id: int, amount: int = 1, db: Session = Depends(get_db), user = Depends(get_current_user)):
    cart = crud_cart.get_cart(db, user.id)
    try:
        item = crud_cart.add_item_to_cart(db, cart.id, product_id, amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product added", "item": _serialize_item(item)}


@api_router.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    item = crud_cart.remove_item_from_cart(db, item_id, user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Product removed from cart"}
