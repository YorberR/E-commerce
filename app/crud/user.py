from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate
from core.security import hash_password
from sqlalchemy import or_


def get_users(db: Session):
    return db.query(User).all()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user: UserCreate) -> User:
    existing_user = db.query(User).filter(or_(User.email == user.email, User.name == user.name)).first()
    if existing_user:
        raise ValueError("User with this email or name already exists")
    hashed_password = hash_password(user.password)
    db_user = User(name=user.name, email=user.email, hashed_password=hashed_password, is_admin=user.is_admin)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
