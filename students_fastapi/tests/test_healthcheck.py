def test_healthcheck(client):
    response = client.get("/api/v1/healthcheck")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
