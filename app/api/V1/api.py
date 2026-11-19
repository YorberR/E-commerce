from fastapi import APIRouter
from api.v1 import auth, products, categories, orders, carts

api_router = APIRouter()

api_router.include_router(auth.api_router, prefix="/auth", tags=["Auth"])
api_router.include_router(products.api_router, prefix="/products", tags=["Products"])
api_router.include_router(categories.api_router, prefix="/categories", tags=["Categories"])
api_router.include_router(carts.api_router, prefix="/cart", tags=["Cart"])
api_router.include_router(orders.api_router, prefix="/orders", tags=["Orders"])
