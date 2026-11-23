from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from crud import cart as crud_cart
from crud.money import ZERO, as_decimal, quantize_money
from deps.deps import get_current_user, get_db
from schemas.cart import (
    CartAddResponse,
    CartItemResponse,
    CartResponse,
    MessageResponse,
)

api_router = APIRouter()


def _item_response(item) -> CartItemResponse:
    unit_price = as_decimal(item.product.price) if item.product else ZERO
    return CartItemResponse(
        id=item.id,
        product_id=item.product_id,
        quantity=item.quantity,
        unit_price=float(unit_price),
        sub_total=float(quantize_money(unit_price * item.quantity)),
    )


def _cart_response(cart) -> CartResponse:
    return CartResponse(
        id=cart.id,
        user_id=cart.user_id,
        total_price=float(as_decimal(cart.total_price)),
        items=[_item_response(item) for item in cart.items],
    )


@api_router.get("/", response_model=CartResponse, summary="View cart contents")
def view_cart(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return _cart_response(crud_cart.get_cart(db, user.id))


@api_router.post(
    "/add/{product_id}",
    response_model=CartAddResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Add a product to the cart",
)
def add_product(
    product_id: int,
    amount: int = Query(default=1, gt=0),
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    cart = crud_cart.get_cart(db, user.id)
    try:
        item = crud_cart.add_item_to_cart(db, cart.id, product_id, amount)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return CartAddResponse(message="Product added", item=_item_response(item))


@api_router.delete(
    "/delete/{item_id}",
    response_model=MessageResponse,
    summary="Remove an item from the cart",
)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    item = crud_cart.remove_item_from_cart(db, item_id, user.id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")
    return MessageResponse(message="Product removed from cart")
