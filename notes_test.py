from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

headers = {}

note_id = 0

@pytest.mark.run(order=3)
def test_create_note():
    global headers
    global note_id
    response = client.post("/token", data={
        "username":"test",
        "password":"hello12345."
    })
    
    token = response.json()["access_token"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = client.post("/createnote",headers=headers, json={
        "title" : "title1",
        "content" : "hello world"
    })
    assert response.status_code == 201
    response_body = response.json()
    assert response_body["title"] == "title1"
    assert response_body["content"] == "hello world"
    note_id = response_body["id"]

    response = client.post("/createnote",headers=headers, json={
        "title" : "title1",
        "content" : "hello world"
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "The data sent is invalid"
    
    response = client.post("/createnote",headers=headers, json={
        "title" : "",
        "content" : "hello world"
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "The data sent is invalid"

    response = client.post("/createnote",headers=headers, json={
        "title" : "title1 ''asd",
        "content" : "hello world"
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "The data sent is invalid"

@pytest.mark.run(order=5)
def test_edit_note():
    response = client.post("/updatenote", headers=headers, json={
        "id" : note_id,
        "title" : "title",
        "content" : "hello world2"
    })
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["title"] == "title"
    assert response_body["content"] == "hello world2"

    response = client.post("/updatenote", headers=headers, json={
        "id" : 0,
        "content" : "hello world"
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["detail"] == "Note with this id not found"

    response = client.post("/updatenote", headers=headers, json={
        "id" : note_id,
        "title" : "",
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "The data sent is invalid"

    response = client.post("/updatenote", headers=headers, json={
        "id" : note_id,
    })
    assert response.status_code == 406
    response_body = response.json()
    assert response_body["detail"] == "The data sent is invalid"

    response = client.post("/updatenote", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb25hdCIsImV4cGlyZXMiOiIyMDIzLTA5LTIxVDA5OjEyOjAwLjI3ODUzMiJ9.COYBjhyUmJ4bwe6Gb-Bd1dseO9kCsnpYO0jLLIRBN4Y"}, json={
        "id" : note_id,
        "title" : "title",
        "content" : "hello world2"
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Could not validate credentials"

@pytest.mark.run(order=6)
def test_get_note():
    response = client.get(f"/note/{note_id}", headers=headers)
    assert response.status_code == 200
    response_body = response.json()
    assert response_body["content"] == "hello world2"
    assert response_body["title"] == "title"

    response = client.get(f"/note/{0}", headers=headers)
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["detail"] == "Note with this id not found"

    response = client.get(f"/note/{note_id}", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb25hdCIsImV4cGlyZXMiOiIyMDIzLTA5LTIxVDA5OjEyOjAwLjI3ODUzMiJ9.COYBjhyUmJ4bwe6Gb-Bd1dseO9kCsnpYO0jLLIRBN4Y"})
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Could not validate credentials"

@pytest.mark.run(order=7)
def test_delete_note():
    response = client.delete("deletenote", headers=headers, json={
        "id":0
    })
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["detail"] == "Note with this id not found"

    response = client.delete("deletenote", headers=headers, json={
        "id":note_id
    })
    assert response.status_code == 202
    response = client.get(f"/note/{note_id}", headers=headers)
    assert response.status_code == 404
    response_body = response.json()
    assert response_body["detail"] == "Note with this id not found"

    response = client.delete("deletenote", headers={"Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJkb25hdCIsImV4cGlyZXMiOiIyMDIzLTA5LTIxVDA5OjEyOjAwLjI3ODUzMiJ9.COYBjhyUmJ4bwe6Gb-Bd1dseO9kCsnpYO0jLLIRBN4Y"},json={
        "id":note_id
    })
    assert response.status_code == 401
    response_body = response.json()
    assert response_body["detail"] == "Could not validate credentials"