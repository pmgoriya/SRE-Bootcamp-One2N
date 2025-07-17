def test_create_student(client, test_student_data):
    response = client.post("/api/v1/students", json=test_student_data)
    assert response.status_code == 200
    data = response.json()

    assert data["first_name"] == test_student_data["first_name"]

    client.delete(f"/api/v1/students/{data['id']}")