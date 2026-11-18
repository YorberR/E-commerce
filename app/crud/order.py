from sqlalchemy.orm import Session
from models.product import Product
from models.order import Shopping_cart, Shopping_cart_item, Order, Order_detail


def _cart_total(db: Session, cart_id: int) -> float:
    """Recalcula el total del carrito a partir de sus items actuales."""
    total = 0.0
    items = db.query(Shopping_cart_item).filter_by(shopping_cart_id=cart_id).all()
    for item in items:
        product = db.get(Product, item.product_id)
        if product and product.price:
            total += product.price * item.quantity
    return total


def get_orders(db: Session, user_id: int):
    return db.query(Order).filter_by(user_id=user_id).order_by(Order.id.desc()).all()


def get_order(db: Session, order_id: int, user_id: int):
    return db.query(Order).filter_by(id=order_id, user_id=user_id).first()


def create_order(db: Session, user_id: int):
    """Convierte el carrito del usuario en una orden.

    Descuenta el stock de cada producto comprado y elimina del carrito solo
    los items que se pudieron comprar. Si ninguno es comprable lanza
    ValueError y no deja rastro (rollback).
    """
    cart = db.query(Shopping_cart).filter_by(user_id=user_id).first()
    if not cart or not cart.items:
        raise ValueError("The cart is empty")

    try:
        order = Order(user_id=user_id, total_price=0)
        db.add(order)
        db.flush()  # obtiene order.id sin cerrar la transacción

        total = 0
        purchased = []
        for item in list(cart.items):
            product = db.get(Product, item.product_id)
            if not product or not product.in_stock or not product.price or product.price <= 0:
                continue

            available = product.stock or 0
            if item.quantity <= 0 or item.quantity > available:
                continue

            subtotal = product.price * item.quantity
            db.add(Order_detail(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                sub_total=subtotal,
            ))
            total += subtotal
            product.stock = available - item.quantity
            if product.stock == 0:
                product.in_stock = False
            purchased.append(item)

        if not purchased:
            raise ValueError("No items in the cart can be purchased")

        for item in purchased:
            db.delete(item)
        db.flush()

        order.total_price = total
        cart.total_price = _cart_total(db, cart.id)
        db.commit()
        db.refresh(order)
        return order
    except Exception:
        db.rollback()
        raise
