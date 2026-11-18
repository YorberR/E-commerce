from sqlalchemy.orm import Session
from models.product import Product
from models.order import Shopping_cart, Shopping_cart_item, Order, Order_detail

def create_order(db:Session, user_id: int):
    cart = db.query(Shopping_cart).filter_by(user_id=user_id).first()
    if  not cart or not cart.items:
        raise ValueError("The cart is empty")
    total = 0
    order = Order(user_id=user_id, total_price=0)
    db.add(order)
    db.commit()
    db.refresh(order)

    for item in cart.items:
        product = db.query(Product).get(item.product_id)
        if product.in_stock is False or product.price <= 0:
            continue
        if item.quantity > 0 and item.quantity <= (product.stock):
            product.stock -= item.quantity
            subtotal = product.price * item.quantity
            detail = Order_detail(order_id = order.id, product_id = product.id, quantity = item.quantity, sub_total = subtotal)
            db.add(detail)
            total += subtotal

    order.total = total
    db.commit()
    for item in cart.items:
        db.delete(item)
    db.commit()
    return order