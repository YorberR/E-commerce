from sqlalchemy.orm import Session
from models.order import Shopping_cart, Shopping_cart_item
from models.product import Product


def _update_cart_total(db: Session, cart_id: int) -> None:
    cart = db.get(Shopping_cart, cart_id)
    if not cart:
        return
    total = 0.0
    for item in cart.items:
        product = db.get(Product, item.product_id)
        if product and product.price:
            total += product.price * item.quantity
    cart.total_price = total
    db.commit()


def get_cart(db: Session, user_id: int):
    cart = db.query(Shopping_cart).filter(Shopping_cart.user_id == user_id).first()
    if not cart:
        cart = Shopping_cart(user_id=user_id, total_price=0)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def add_item_to_cart(db: Session, cart_id: int, product_id: int, quantity: int):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    product = db.get(Product, product_id)
    if not product:
        raise ValueError("Product not found")
    if not product.in_stock or (product.stock or 0) <= 0:
        raise ValueError("Product is out of stock")

    item = db.query(Shopping_cart_item).filter_by(
        shopping_cart_id=cart_id, product_id=product_id
    ).first()
    new_quantity = quantity + (item.quantity if item else 0)
    if new_quantity > (product.stock or 0):
        raise ValueError("Not enough stock for the requested quantity")

    if item:
        item.quantity = new_quantity
    else:
        item = Shopping_cart_item(
            shopping_cart_id=cart_id, product_id=product_id, quantity=quantity
        )
        db.add(item)
    db.commit()
    db.refresh(item)
    _update_cart_total(db, cart_id)
    return item


def remove_item_from_cart(db: Session, item_id: int, user_id: int):
    item = db.query(Shopping_cart_item).join(
        Shopping_cart, Shopping_cart_item.shopping_cart_id == Shopping_cart.id
    ).filter(
        Shopping_cart_item.id == item_id,
        Shopping_cart.user_id == user_id,
    ).first()
    if not item:
        return None
    cart_id = item.shopping_cart_id
    db.delete(item)
    db.commit()
    _update_cart_total(db, cart_id)
    return item
