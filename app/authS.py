from jose import JWTError, jwt
from datetime import datetime, timedelta
from pydantic_settings import BaseSettings
from config import settings

def create_access_token(sub: str, es_admin: bool):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data = {"sub": sub, "is_admin": es_admin, "exp": expire}
    token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token

def verify_token(token: str):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None