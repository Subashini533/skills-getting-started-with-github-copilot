from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert isinstance(data["Chess Club"]["participants"], list)


def test_signup_success():
    # Use a new email
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Check if added
    response = client.get("/activities")
    data = response.json()
    assert "newstudent@mergington.edu" in data["Chess Club"]["participants"]


def test_signup_duplicate():
    # First signup
    client.post("/activities/Programming Class/signup", params={"email": "dup@mergington.edu"})
    # Second should fail
    response = client.post("/activities/Programming Class/signup", params={"email": "dup@mergington.edu"})
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_invalid_activity():
    response = client.post("/activities/Invalid Activity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success():
    # First signup
    client.post("/activities/Soccer Club/signup", params={"email": "removeme@mergington.edu"})
    # Then remove
    response = client.delete("/activities/Soccer Club/signup", params={"email": "removeme@mergington.edu"})
    assert response.status_code == 200
    assert "Unregistered" in response.json()["message"]

    # Check if removed
    response = client.get("/activities")
    data = response.json()
    assert "removeme@mergington.edu" not in data["Soccer Club"]["participants"]


def test_unregister_not_registered():
    response = client.delete("/activities/Chess Club/signup", params={"email": "notregistered@mergington.edu"})
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]


def test_unregister_invalid_activity():
    response = client.delete("/activities/Invalid Activity/signup", params={"email": "test@mergington.edu"})
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
