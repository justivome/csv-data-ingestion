import os

SAMPLE_CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "example", "sales_data_sample.csv")


def _register_and_get_token(client, email="test@example.com"):
    res = client.post("/api/register", json={
        "name": "Test User",
        "email": email,
        "password": "password123",
    })
    return res.json()["access_token"]


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


def _upload_sample(client, token):
    with open(SAMPLE_CSV_PATH, "rb") as f:
        return client.post(
            "/api/upload",
            files={"file": ("sales_data_sample.csv", f, "text/csv")},
            headers=_auth_headers(token),
        )


def test_upload_returns_stats(client):
    token = _register_and_get_token(client)
    response = _upload_sample(client, token)
    assert response.status_code == 200
    data = response.json()
    assert "dataset_id" in data
    assert "row_count" in data
    assert "total_sales" in data
    assert "date_range" in data


def test_upload_without_auth_returns_401(client):
    with open(SAMPLE_CSV_PATH, "rb") as f:
        response = client.post(
            "/api/upload",
            files={"file": ("sales_data_sample.csv", f, "text/csv")},
        )
    assert response.status_code == 401


def test_list_datasets(client):
    token = _register_and_get_token(client)
    _upload_sample(client, token)
    response = client.get("/api/datasets", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert len(data["datasets"]) == 1


def test_get_dataset_detail(client):
    token = _register_and_get_token(client)
    upload = _upload_sample(client, token)
    dataset_id = upload.json()["dataset_id"]
    response = client.get(f"/api/datasets/{dataset_id}", headers=_auth_headers(token))
    assert response.status_code == 200
    data = response.json()
    assert "records" in data
    assert "aggregates" in data
    assert len(data["records"]) <= data["page_size"]


def test_user_cannot_access_other_users_dataset(client):
    token1 = _register_and_get_token(client, "user1@example.com")
    upload = _upload_sample(client, token1)
    dataset_id = upload.json()["dataset_id"]

    token2 = _register_and_get_token(client, "user2@example.com")
    response = client.get(f"/api/datasets/{dataset_id}", headers=_auth_headers(token2))
    assert response.status_code == 404
