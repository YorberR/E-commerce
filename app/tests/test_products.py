PRODUCTS_URL = "/api/v1/products/"


def product_payload(category_id: int, **overrides) -> dict:
    data = {
        "name": "laptop",
        "description": "test product",
        "price": 20.0,
        "in_stock": True,
        "stock": 40,
        "category_id": category_id,
    }
    data.update(overrides)
    return data


def test_create_product_requires_token(client, category):
    response = client.post(PRODUCTS_URL, json=product_payload(category.id))

    assert response.status_code == 401


def test_create_product_forbidden_for_non_admin(client, category, user_headers):
    response = client.post(
        PRODUCTS_URL,
        json=product_payload(category.id),
        headers=user_headers,
    )

    assert response.status_code == 403


def test_create_successful_product(client, category, admin_headers):
    data = product_payload(category.id)

    response = client.post(PRODUCTS_URL, json=data, headers=admin_headers)

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == data["name"]
    assert body["price"] == data["price"]
    assert body["stock"] == data["stock"]
    assert "id" in body


def test_product_listing(client, category, admin_headers):
    created = client.post(
        PRODUCTS_URL,
        json=product_payload(category.id),
        headers=admin_headers,
    ).json()

    response = client.get(PRODUCTS_URL)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(product["id"] == created["id"] for product in body)


def test_update_product(client, category, admin_headers):
    created = client.post(
        PRODUCTS_URL,
        json=product_payload(category.id),
        headers=admin_headers,
    ).json()

    response = client.put(
        f"{PRODUCTS_URL}{created['id']}",
        json=product_payload(category.id, name="laptop pro", price=30.0, stock=5),
        headers=admin_headers,
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "laptop pro"
    assert body["price"] == 30.0
    assert body["stock"] == 5


def test_delete_product(client, category, admin_headers):
    created = client.post(
        PRODUCTS_URL,
        json=product_payload(category.id),
        headers=admin_headers,
    ).json()

    response = client.delete(f"{PRODUCTS_URL}{created['id']}", headers=admin_headers)

    assert response.status_code == 200
    ids = [product["id"] for product in client.get(PRODUCTS_URL).json()]
    assert created["id"] not in ids


def test_create_product_without_stock_defaults_to_zero(client, category, admin_headers):
    data = product_payload(category.id)
    data.pop("stock")

    response = client.post(PRODUCTS_URL, json=data, headers=admin_headers)

    assert response.status_code == 200, response.text
    assert response.json()["stock"] == 0
