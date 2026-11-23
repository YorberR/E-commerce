from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError

from api.v1.api import api_router
from core.exceptions import ConflictError

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
        "Portfolio": "https://yorberrojas.me/",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
)


@app.exception_handler(ConflictError)
async def conflict_error_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    return JSONResponse(
        status_code=409,
        content={"detail": "The operation conflicts with existing data"},
    )


app.include_router(api_router, prefix="/api/v1")
