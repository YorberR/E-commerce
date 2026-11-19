def test_invalid_login(client):
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "example@gmail.com", "password": "123"},
    )

    assert response.status_code == 401


def test_ping_docs(client):
    response = client.get("/docs")

    assert response.status_code == 200


def test_admin_login_returns_token(admin_headers):
    assert admin_headers["Authorization"].startswith("Bearer ")


def test_current_user(client, admin_headers):
    response = client.get("/api/v1/auth/users/me", headers=admin_headers)

    assert response.status_code == 200
    assert response.json()["email"] == "admin@test.com"
