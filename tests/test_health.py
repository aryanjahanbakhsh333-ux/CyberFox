from main import app


def test_health_endpoint():
    client = app.test_client()

    response = client.get(
        "/api/system/health"
    )

    assert response.status_code == 200

    data = response.get_json()

    assert data is not None
    assert "status" in data
