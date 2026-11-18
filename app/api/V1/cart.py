from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import cart as crud_cart
from deps.deps import get_db, get_current_user

api_router = APIRouter()


@api_router.get("/", summary="view cart contents")
def view_cart(db: Session = Depends(get_db), user = Depends(get_current_user)):
    return crud_cart.get_cart(db, user.id)


@api_router.post("/add/{product_id}")
def add_product(product_id: int, amount: int = 1, db: Session = Depends(get_db), user = Depends(get_current_user)):
    cart = crud_cart.get_cart(db, user.id)
    try:
        item = crud_cart.add_item_to_cart(db, cart.id, product_id, amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Product added", "item": item}


@api_router.delete("/delete/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db), user = Depends(get_current_user)):
    item = crud_cart.remove_item_from_cart(db, item_id, user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return {"message": "Product removed from cart"}
