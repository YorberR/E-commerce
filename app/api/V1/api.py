from fastapi import APIRouter
from api.V1 import auth, products, categories, cart, orden

api_router = APIRouter()

api_router.include_router(auth.api_router, prefix="/auth", tags=["Auth"])
api_router.include_router(products.api_router, prefix="/products", tags=["Products"])
api_router.include_router(categories.api_router, prefix="/categories", tags=["Categories"])
api_router.include_router(cart.api_router, prefix="/carts", tags=["Carts"])
api_router.include_router(orden.api_router, prefix="/ordens", tags=["Ordens"])