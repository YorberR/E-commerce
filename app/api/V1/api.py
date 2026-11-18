from fastapi import APIRouter
from api.V1 import auth, products, categories, cart, orders

api_router = APIRouter()

api_router.include_router(auth.api_router, prefix="/auth", tags=["Auth"])
api_router.include_router(products.api_router, prefix="/products", tags=["Products"])
api_router.include_router(categories.api_router, prefix="/categories", tags=["Categories"])
api_router.include_router(cart.api_router, prefix="/cart", tags=["Cart"])
api_router.include_router(orders.api_router, prefix="/orders", tags=["Orders"])
