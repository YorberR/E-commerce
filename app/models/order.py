from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from db.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Shopping_cart(Base):
    __tablename__ = "shopping_carts"
    __table_args__ = (
        CheckConstraint("total_price >= 0", name="ck_shopping_carts_total_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    total_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0",
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        unique=True,
    )
    user = relationship("User", back_populates="shopping_carts")
    items = relationship(
        "Shopping_cart_item",
        back_populates="shopping_cart",
        cascade="all, delete-orphan",
    )


class Shopping_cart_item(Base):
    __tablename__ = "shopping_cart_items"
    __table_args__ = (
        UniqueConstraint(
            "shopping_cart_id",
            "product_id",
            name="uq_shopping_cart_items_cart_product",
        ),
        CheckConstraint("quantity > 0", name="ck_shopping_cart_items_quantity_positive"),
    )

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, default=1, nullable=False)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    shopping_cart_id = Column(
        Integer,
        ForeignKey("shopping_carts.id", ondelete="CASCADE"),
        nullable=False,
    )
    shopping_cart = relationship("Shopping_cart", back_populates="items")
    product = relationship("Product")


class Order(Base):
    __tablename__ = "orders"
    __table_args__ = (
        CheckConstraint("total_price >= 0", name="ck_orders_total_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    total_price = Column(
        Numeric(10, 2),
        nullable=False,
        default=Decimal("0.00"),
        server_default="0",
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    detail = relationship(
        "Order_detail",
        back_populates="order",
        cascade="all, delete-orphan",
    )


class Order_detail(Base):
    __tablename__ = "order_details"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="ck_order_details_quantity_positive"),
        CheckConstraint("sub_total >= 0", name="ck_order_details_sub_total_non_negative"),
    )

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    quantity = Column(Integer, default=1, nullable=False)
    sub_total = Column(Numeric(10, 2), nullable=False)
    order = relationship("Order", back_populates="detail")
    product = relationship("Product")
