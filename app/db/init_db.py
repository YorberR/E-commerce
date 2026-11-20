"""Create the database schema directly from the SQLAlchemy models.

Run from the `app/` directory:

    python -m db.init_db

This is the supported bootstrap path for a fresh database. See AUDIT.md
(finding C1) for why the current Alembic history cannot provision an empty
database on its own.
"""

from db.database import Base, engine

from models.user import User  # noqa: F401
from models.category import Category  # noqa: F401
from models.product import Product  # noqa: F401
from models.order import (  # noqa: F401
    Order,
    Order_detail,
    Shopping_cart,
    Shopping_cart_item,
)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()
    print("Database schema created.")
