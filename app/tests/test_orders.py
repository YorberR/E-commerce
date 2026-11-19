ORDERS_URL = "/api/v1/orders/"
CHECKOUT_URL = "/api/v1/orders/checkout"
CART_URL = "/api/v1/cart/"
ADD_URL = "/api/v1/cart/add/{product_id}"

from models.product import Product


def add_to_cart(client, headers, product_id, amount=1):
    response = client.post(
        ADD_URL.format(product_id=product_id),
        params={"amount": amount},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response


def test_checkout_requires_auth(client):
    response = client.post(CHECKOUT_URL)

    assert response.status_code == 401


def test_checkout_with_empty_cart_returns_400(client, user_headers):
    response = client.post(CHECKOUT_URL, headers=user_headers)

    assert response.status_code == 400
    assert "empty" in response.json()["detail"].lower()


def test_checkout_creates_order_and_empties_cart(client, product, db_session, user_headers):
    add_to_cart(client, user_headers, product.id, amount=2)

    response = client.post(CHECKOUT_URL, headers=user_headers)

    assert response.status_code == 201, response.text
    body = response.json()
    assert body["total_price"] == 50.0
    assert body["details"] == [
        {"product_id": product.id, "quantity": 2, "sub_total": 50.0}
    ]

    assert db_session.get(Product, product.id).stock == 8
    cart = client.get(CART_URL, headers=user_headers).json()
    assert cart["items"] == []


def test_checkout_decrements_stock_to_zero_and_marks_out_of_stock(client, product, db_session, user_headers):
    add_to_cart(client, user_headers, product.id, amount=product.stock)

    response = client.post(CHECKOUT_URL, headers=user_headers)

    assert response.status_code == 201, response.text
    updated = db_session.get(Product, product.id)
    assert updated.stock == 0
    assert updated.in_stock is False


def test_checkout_with_insufficient_stock_does_not_change_data(client, product, db_session, user_headers):
    add_to_cart(client, user_headers, product.id, amount=3)
    # stock changes after the item was added to the cart
    product.stock = 1
    db_session.commit()

    response = client.post(CHECKOUT_URL, headers=user_headers)

    assert response.status_code == 400
    assert client.get(ORDERS_URL, headers=user_headers).json() == []
    assert db_session.get(Product, product.id).stock == 1
    assert len(client.get(CART_URL, headers=user_headers).json()["items"]) == 1


def test_list_orders_only_returns_own_orders(client, product, user_headers, admin_headers):
    add_to_cart(client, user_headers, product.id, amount=1)
    client.post(CHECKOUT_URL, headers=user_headers)

    own_orders = client.get(ORDERS_URL, headers=user_headers).json()
    admin_orders = client.get(ORDERS_URL, headers=admin_headers).json()

    assert len(own_orders) == 1
    assert admin_orders == []


def test_get_order_from_another_user_returns_404(client, product, user_headers, admin_headers):
    add_to_cart(client, user_headers, product.id, amount=1)
    order = client.post(CHECKOUT_URL, headers=user_headers).json()

    own = client.get(f"{ORDERS_URL}{order['id']}", headers=user_headers)
    other = client.get(f"{ORDERS_URL}{order['id']}", headers=admin_headers)

    assert own.status_code == 200
    assert own.json()["total_price"] == 25.0
    assert other.status_code == 404


def test_get_missing_order_returns_404(client, user_headers):
    response = client.get(f"{ORDERS_URL}9999", headers=user_headers)

    assert response.status_code == 404
