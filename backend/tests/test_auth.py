def test_register_returns_token(client):
    response = client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_register_duplicate_email_returns_error(client):
    payload = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
    }
    client.post("/api/register", json=payload)
    response = client.post("/api/register", json=payload)
    assert response.status_code == 409


def test_login_valid_credentials_returns_token(client):
    client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


def test_login_wrong_password_returns_401(client):
    client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/login",
        json={
            "email": "test@example.com",
            "password": "wrongpassword",
        },
    )
    assert response.status_code == 401


def test_me_with_valid_token_returns_user(client):
    reg = client.post(
        "/api/register",
        json={
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
        },
    )
    token = reg.json()["access_token"]
    response = client.get("/api/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data


def test_me_without_token_returns_401(client):
    response = client.get("/api/me")
    assert response.status_code == 401
