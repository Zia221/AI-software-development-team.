from fastapi.testclient import TestClient

from api import app


client = TestClient(app)


def test_empty_project():

    response = client.post(
        "/projects",
        json={
            "project_idea": "   "
        }
    )

    assert response.status_code == 400

    assert response.json()["detail"] == (
        "Project idea cannot be empty."
    )