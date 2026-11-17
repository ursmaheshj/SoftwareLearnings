from fastapi.testclient import TestClient
from asyncfastgeek.main import app

client = TestClient(app)

def test_envvars():
    response = client.get("/api/profile/envvars")
    assert response.status_code == 200
    assert response.json() == { "db_username": "ExampleUser", "db_password": "ExamplePassword" }