CATEGORIES_URL = "/api/v1/categories/"


def test_create_category_requires_token(client):
    response = client.post(CATEGORIES_URL, json={"name": "Electronics"})

    assert response.status_code == 401


def test_create_category_forbidden_for_non_admin(client, user_headers):
    response = client.post(
        CATEGORIES_URL,
        json={"name": "Electronics"},
        headers=user_headers,
    )

    assert response.status_code == 403


def test_create_successful_category(client, admin_headers):
    response = client.post(
        CATEGORIES_URL,
        json={"name": "Electronics"},
        headers=admin_headers,
    )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["name"] == "Electronics"
    assert "id" in body


def test_category_listing(client, admin_headers):
    created = client.post(
        CATEGORIES_URL,
        json={"name": "Home"},
        headers=admin_headers,
    ).json()

    response = client.get(CATEGORIES_URL)

    assert response.status_code == 200
    body = response.json()
    assert isinstance(body, list)
    assert any(category["id"] == created["id"] for category in body)


def test_update_category(client, admin_headers):
    created = client.post(
        CATEGORIES_URL,
        json={"name": "Home"},
        headers=admin_headers,
    ).json()

    response = client.put(
        f"{CATEGORIES_URL}{created['id']}",
        json={"name": "Home & Kitchen"},
        headers=admin_headers,
    )

    assert response.status_code == 200, response.text
    assert response.json()["name"] == "Home & Kitchen"


def test_update_missing_category_returns_404(client, admin_headers):
    response = client.put(
        f"{CATEGORIES_URL}9999",
        json={"name": "Does not exist"},
        headers=admin_headers,
    )

    assert response.status_code == 404


def test_delete_category(client, admin_headers):
    created = client.post(
        CATEGORIES_URL,
        json={"name": "Temporary"},
        headers=admin_headers,
    ).json()

    response = client.delete(f"{CATEGORIES_URL}{created['id']}", headers=admin_headers)

    assert response.status_code == 200
    ids = [category["id"] for category in client.get(CATEGORIES_URL).json()]
    assert created["id"] not in ids


def test_delete_missing_category_returns_404(client, admin_headers):
    response = client.delete(f"{CATEGORIES_URL}9999", headers=admin_headers)

    assert response.status_code == 404
