from fastapi.testclient import TestClient
from sistema import app

# Cliente de teste
client = TestClient(app)

# Obter token JWT válido
def get_valid_token():
    response = client.post(
        "/token",
        json={"username": "admin", "password": "admin"}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

# Token válido para autenticação
valid_token = get_valid_token()

def test_create_task():
    response = client.post(
        "/tasks",
        json={
            "title": "Test Task",
            "description": "This is a test task.",
            "status": "pending",
            "due_date": "2025-01-31"
        },
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task created successfully!"

def test_read_tasks():
    response = client.get("/tasks", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_task():
    response = client.put(
        "/tasks/1",
        json={
            "title": "Updated Task",
            "description": "This task has been updated.",
            "status": "completed",
            "due_date": "2025-02-01"
        },
        headers={"Authorization": f"Bearer {valid_token}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Task updated successfully!"

def test_delete_task():
    response = client.delete("/tasks/1", headers={"Authorization": f"Bearer {valid_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Task deleted successfully!"
