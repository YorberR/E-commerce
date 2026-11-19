CART_URL = "/api/v1/cart/"
ADD_URL = "/api/v1/cart/add/{product_id}"
DELETE_URL = "/api/v1/cart/delete/{item_id}"


def add_to_cart(client, headers, product_id, amount=1):
    return client.post(
        ADD_URL.format(product_id=product_id),
        params={"amount": amount},
        headers=headers,
    )


def test_view_cart_requires_auth(client):
    response = client.get(CART_URL)

    assert response.status_code == 401


def test_view_cart_starts_empty(client, user_headers):
    response = client.get(CART_URL, headers=user_headers)

    assert response.status_code == 200
    body = response.json()
    assert body["items"] == []
    assert body["total_price"] == 0


def test_add_product_to_cart(client, product, user_headers):
    response = add_to_cart(client, user_headers, product.id, amount=2)

    assert response.status_code == 200, response.text
    assert response.json()["item"]["quantity"] == 2

    cart = client.get(CART_URL, headers=user_headers).json()
    assert len(cart["items"]) == 1
    assert cart["items"][0]["product_id"] == product.id
    assert cart["items"][0]["unit_price"] == 25.0
    assert cart["items"][0]["sub_total"] == 50.0
    assert cart["total_price"] == 50.0


def test_adding_same_product_accumulates_quantity(client, product, user_headers):
    add_to_cart(client, user_headers, product.id, amount=1)
    add_to_cart(client, user_headers, product.id, amount=2)

    cart = client.get(CART_URL, headers=user_headers).json()

    assert len(cart["items"]) == 1
    assert cart["items"][0]["quantity"] == 3
    assert cart["total_price"] == 75.0


def test_add_more_than_available_stock(client, product, user_headers):
    response = add_to_cart(client, user_headers, product.id, amount=product.stock + 1)

    assert response.status_code == 400
    assert "stock" in response.json()["detail"].lower()


def test_add_out_of_stock_product(client, product, db_session, user_headers):
    product.stock = 0
    db_session.commit()

    response = add_to_cart(client, user_headers, product.id)

    assert response.status_code == 400


def test_add_unknown_product(client, user_headers):
    response = add_to_cart(client, user_headers, 9999)

    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()


def test_add_invalid_amount(client, product, user_headers):
    response = add_to_cart(client, user_headers, product.id, amount=0)

    assert response.status_code == 400


def test_remove_item_from_cart(client, product, user_headers):
    add_to_cart(client, user_headers, product.id, amount=2)
    cart = client.get(CART_URL, headers=user_headers).json()

    response = client.delete(
        DELETE_URL.format(item_id=cart["items"][0]["id"]),
        headers=user_headers,
    )

    assert response.status_code == 200
    cart = client.get(CART_URL, headers=user_headers).json()
    assert cart["items"] == []
    assert cart["total_price"] == 0


def test_cannot_remove_item_from_another_user(client, product, user_headers, other_headers):
    add_to_cart(client, user_headers, product.id, amount=1)
    item_id = client.get(CART_URL, headers=user_headers).json()["items"][0]["id"]

    response = client.delete(DELETE_URL.format(item_id=item_id), headers=other_headers)

    assert response.status_code == 404
    assert len(client.get(CART_URL, headers=user_headers).json()["items"]) == 1


def test_remove_missing_item_returns_404(client, user_headers):
    response = client.delete(DELETE_URL.format(item_id=9999), headers=user_headers)

    assert response.status_code == 404
