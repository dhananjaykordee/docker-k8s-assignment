from fastapi.testclient import TestClient

from app import app


def test_root_redirects_to_docs():
    with TestClient(app) as client:
        response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
