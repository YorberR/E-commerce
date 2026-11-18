from sqlalchemy.orm import Session
from models.order import Shopping_cart, Shopping_cart_item

def get_cart(db: Session, user_id: int):
    cart = db.query(Shopping_cart).filter(Shopping_cart.user_id == user_id).first()
    if not cart:
        cart = Shopping_cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

def add_item_to_cart(db: Session, cart_id: int, product_id: int, quantity: int = 1):
    item = db.query(Shopping_cart_item).filter(Shopping_cart_item.cart_id == cart_id, Shopping_cart_item.product_id == product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = Shopping_cart_item(shopping_cart_id=cart_id, product_id=product_id, quantity=quantity)
        db.add(item)
    db.commit()
    db.refresh(item)
    return item

def remove_item_from_cart(db: Session, item_id: int):
    item = db.query(Shopping_cart_item).get(item_id)
    if item:
        db.delete(item)
        db.commit()