def test_create_task_rejects_title_containing_only_whitespace(client):
    response = client.post("/tasks", json={"title": "   "})

    assert response.status_code == 422
