from fastapi.testclient import TestClient
import pytest
from main import app

client = TestClient(app)

headers = {}

@pytest.mark.run(order=1)
def test_register():
    response = client.post("/register", json={
        "username": "test",
        "password": "hello12345."
    })
    assert response.status_code == 201
    response_body = response.json()
    assert response_body["username"] == "test"

    response = client.response = client.post("/register", json={
        "username": "test",
        "password": "hello12345."
    })
    assert response.status_code == 409
    response_body = response.json()
    assert response_body["detail"] == "Username is already in use"

    response = client.response = client.post("/register", json={
        "username": "test /",
        "password": "hello12345"
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "Username is not acceptable"

    response = client.response = client.post("/register", json={
        "username": "test_not_yet_existing",
        "password": "123"
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "Password is too short it must be 6 characters"

@pytest.mark.run(order=2)
def test_login():
    global headers
    response = client.post("/token", data={
        "username":"test",
        "password":"hello12345."
    })
    assert response.status_code == 201
    response_body = response.json()
    assert response_body["access_token"] != "" or response_body["token_type"] == "bearer"
    token = response_body["access_token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = client.post("/token", data={
        "username":"test_not_exist",
        "password":"hello12345."
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Incorrect username or password"

    response = client.post("/token", data={
        "username":"test",
        "password":"helloee"
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Incorrect username or password"

