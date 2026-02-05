from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_upload_image_success():
    response = client.post(
        "/images/upload?user_id=user_123&tags=test,localstack",
        files={
            "file": ("test.jpg", b"fake-image-content", "image/jpeg")
        }
    )

    assert response.status_code == 200
    body = response.json()
    assert "image_id" in body
    assert isinstance(body["image_id"], str)


def test_upload_image_missing_file():
    response = client.post(
        "/images/upload?user_id=user_123"
    )

    # FastAPI validation error
    assert response.status_code == 422


def test_upload_image_missing_user_id():
    response = client.post(
        "/images/upload",
        files={
            "file": ("test.jpg", b"fake-image-content", "image/jpeg")
        }
    )

    assert response.status_code == 422


def test_upload_image_empty_tags():
    response = client.post(
        "/images/upload?user_id=user_123",
        files={
            "file": ("test.jpg", b"fake-image-content", "image/jpeg")
        }
    )

    assert response.status_code == 200
    assert "image_id" in response.json()
