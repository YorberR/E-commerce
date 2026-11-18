"""Funciones CRUD disponibles como `crud.<nombre>`."""

from crud.user import create_user, get_user, get_user_by_email, get_users
from crud.category import (
    create_category,
    delete_category,
    get_categories,
    get_category,
    update_category,
)
from crud.product import (
    create_product,
    delete_product,
    get_product,
    get_products,
    update_product,
)
from crud.cart import add_item_to_cart, get_cart, remove_item_from_cart
from crud.order import create_order, get_order, get_orders

__all__ = [
    "create_user",
    "get_user",
    "get_user_by_email",
    "get_users",
    "create_category",
    "delete_category",
    "get_categories",
    "get_category",
    "update_category",
    "create_product",
    "delete_product",
    "get_product",
    "get_products",
    "update_product",
    "add_item_to_cart",
    "get_cart",
    "remove_item_from_cart",
    "create_order",
    "get_order",
    "get_orders",
]
