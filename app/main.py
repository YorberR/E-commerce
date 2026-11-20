from fastapi import FastAPI
from api.v1.api import api_router

app = FastAPI(
    title="E-commerce API",
    description=""" 
    RESTful API for E-commerce management

    Includes:
    - Authentication with JWT
    - Product and category management
    - Shopping cart
    - Order management
    """,
    version="1.0.0",
    contact={
        "developer": "Yorber Rojas",
        "Repository": "https://github.com/YorberR/E-commerce",
        "Portfolio": "https://yorberrojas.me/"
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT"
    }
)

app.include_router(api_router, prefix="/api/v1")