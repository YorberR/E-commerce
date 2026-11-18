from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    in_stock = Column(Boolean, default=True, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"))
    stock = Column(Integer, default=0, server_default="0", nullable=False)

    categories = relationship("Category", back_populates="products")