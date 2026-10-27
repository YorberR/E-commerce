from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import datetime

class Shopping_cart(Base):
    __tablename__ = "shopping_carts"
    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="shopping_carts")
    items = relationship("Shopping_cart_item", back_populates="shopping_cart", cascade="all, delete")

class Shopping_cart_item(Base):
    __tablename__ = "shopping_cart_items"
    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1)
    product_id = Column(Integer, ForeignKey("products.id"))
    shopping_cart_id = Column(Integer, ForeignKey("shopping_carts.id"))
    shopping_cart = relationship("Shopping_cart", back_populates="items")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.now)
    total_price = Column(Float)
    user_id = Column(Integer, ForeignKey("users.id"))
    detail = relationship("Order_detail", back_populates="order")

class Order_detail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    sub_total = Column(Float)
    order = relationship("Order", back_populates="detail")
    product = relationship("Product")