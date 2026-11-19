"""Shared fixtures for the test suite.

Every test runs against an in-memory SQLite database, so it never touches
the PostgreSQL database or leaves data behind. Users and tokens are created
automatically: no need to paste tokens by hand into each test file.
"""

import sys
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from db.database import Base
from deps.deps import get_db
from crud import user as crud_user
from schemas.user import UserCreate
from main import app

from models.user import User          # noqa: F401  (registra las tablas)
from models.category import Category
from models.product import Product    # noqa: F401
from models.order import Shopping_cart, Shopping_cart_item, Order, Order_detail  # noqa: F401


ADMIN_EMAIL = "admin@test.com"
ADMIN_PASSWORD = "admin123"
USER_EMAIL = "user@test.com"
USER_PASSWORD = "user123"
OTHER_EMAIL = "other@test.com"
OTHER_PASSWORD = "other123"


@pytest.fixture()
def db_session():
    """Session bound to an isolated in-memory SQLite database per test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine, autoflush=False)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


@pytest.fixture()
def client(db_session):
    """TestClient con la dependencia get_db apuntando a la BD de test."""
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def admin_user(db_session):
    return crud_user.create_user(
        db_session,
        UserCreate(name="admin", email=ADMIN_EMAIL, password=ADMIN_PASSWORD, is_admin=True),
    )


@pytest.fixture()
def normal_user(db_session):
    return crud_user.create_user(
        db_session,
        UserCreate(name="user", email=USER_EMAIL, password=USER_PASSWORD, is_admin=False),
    )


@pytest.fixture()
def category(db_session):
    category = Category(name="test-category")
    db_session.add(category)
    db_session.commit()
    db_session.refresh(category)
    return category


@pytest.fixture()
def product(db_session, category):
    product = Product(
        name="shirt",
        description="test product",
        price=25.0,
        in_stock=True,
        stock=10,
        category_id=category.id,
    )
    db_session.add(product)
    db_session.commit()
    db_session.refresh(product)
    return product


@pytest.fixture()
def other_user(db_session):
    return crud_user.create_user(
        db_session,
        UserCreate(name="other", email=OTHER_EMAIL, password=OTHER_PASSWORD, is_admin=False),
    )


def _login(client: TestClient, email: str, password: str) -> dict:
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )
    assert response.status_code == 200, response.text
    return {"Authorization": f"Bearer {response.json()['access_token']}"}


@pytest.fixture()
def admin_headers(client, admin_user):
    """Authorization header ready to use in any request."""
    return _login(client, ADMIN_EMAIL, ADMIN_PASSWORD)


@pytest.fixture()
def user_headers(client, normal_user):
    """Header for a regular user (no admin permissions)."""
    return _login(client, USER_EMAIL, USER_PASSWORD)


@pytest.fixture()
def other_headers(client, other_user):
    """Header for a second user, used to test data ownership."""
    return _login(client, OTHER_EMAIL, OTHER_PASSWORD)
