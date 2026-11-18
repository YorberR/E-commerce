from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from deps.deps import get_db, get_current_user
from fastapi import APIRouter
from crud.order import Order as crud_orden

api_router = APIRouter()

@api_router.post("/confirm")
def confirm_orden(db:Session = Depends(get_db), user = Depends(get_current_user)):
    try:
        orden = crud_orden.create_order(db, user.id)
        return {
            "message": "Order generated", 
            "orden_id": orden.id,
            "total": orden.total
            }
    except ValueError as e:
        raise HTTPException(status_code=400, datail=str(e))

