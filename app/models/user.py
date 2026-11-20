from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    shopping_carts = relationship(
        "Shopping_cart", back_populates="user", cascade="all, delete-orphan"
    )

    @property
    def cart(self):
        """Shortcut to the user's first cart (None if there is none)."""
        return self.shopping_carts[0] if self.shopping_carts else None
