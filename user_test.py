from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

headers = {}

@pytest.mark.run(order=4)
def test_get_user():
    global headers
    response = client.post("/token", data={
        "username":"test",
        "password":"hello12345."
    })
    
    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.get("/user", headers=headers)
    assert response.status_code == 200
    response_body = response.json()
    assert len(response_body["notes"]) == 1
    
    response = client.get("/user", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb25hdCIsImV4cGlyZXMiOiIyMDIzLTA5LTIxVDA5OjEyOjAwLjI3ODUzMiJ9.COYBjhyUmJ4bwe6Gb-Bd1dseO9kCsnpYO0jLLIRBN4Y"}, json={
        "username":"test",
        "password":"hello12345."
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Could not validate credentials"

@pytest.mark.run(order=8)
def test_delete_user():
    response = client.delete("/deletelogin", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb25hdCIsImV4cGlyZXMiOiIyMDIzLTA5LTIxVDA5OjEyOjAwLjI3ODUzMiJ9.COYBjhyUmJ4bwe6Gb-Bd1dseO9kCsnpYO0jLLIRBN4Y"}, json={
        "username":"test",
        "password":"hello12345."
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Could not validate credentials"

    response = client.delete("/deletelogin", headers=headers, json={
        "username":"test",
        "password":"hello2222"
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Incorrect username or password"

    response = client.delete("/deletelogin", headers=headers,json={
        "username":"test",
        "password":"hello12345."
    })
    assert response.status_code == 202