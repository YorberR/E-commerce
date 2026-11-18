from sqlalchemy.orm import Session
from models.category import Category
from schemas.category import CategoryCreate

def create_category(db: Session, category: CategoryCreate):
    db_category = Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(Category).all()

def get_category(db: Session, category_id: int):
    return db.query(Category).filter(Category.id == category_id).first()

def update_category(db: Session, category_id: int, data: CategoryCreate):
    category = get_category(db, category_id)
    if category:
        for key, value in data.model_dump().items():
            setattr(category, key, value)
        db.commit()
        db.refresh(category)
    return category

def delete_category(db: Session, category_id: int):
    category = get_category(db, category_id)
    if category:
        db.delete(category)
        db.commit()
    return category
