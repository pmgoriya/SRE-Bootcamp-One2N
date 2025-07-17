def test_update_student(client, test_student_data):
    created = client.post("/api/v1/students", json=test_student_data).json()
    student_id = created["id"]

    patch_data = {"first_name": "Updated"}
    response = client.patch(f"/api/v1/students/{student_id}", json=patch_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == "Updated"

    client.delete(f"/api/v1/students/{student_id}")
