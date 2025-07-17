def test_get_students(client):
    response = client.get("/api/v1/students")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
