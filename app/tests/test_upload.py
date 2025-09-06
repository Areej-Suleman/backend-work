import pytest
from fastapi.testclient import TestClient
import io
from PIL import Image

def create_test_image():
    """Create a test image file."""
    image = Image.new('RGB', (100, 100), color='red')
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes

def test_upload_image(client: TestClient, test_user_data):
    """Test image upload endpoint."""
    # Register and login
    client.post("/api/v1/auth/register", json=test_user_data)
    login_response = client.post("/api/v1/auth/login", data={
        "username": test_user_data["email"],
        "password": test_user_data["password"]
    })
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Upload image
    test_image = create_test_image()
    files = {"file": ("test.jpg", test_image, "image/jpeg")}
    response = client.post("/api/v1/upload/", files=files, headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert "file_id" in data
    assert "filename" in data

def test_upload_without_auth(client: TestClient):
    """Test upload without authentication."""
    test_image = create_test_image()
    files = {"file": ("test.jpg", test_image, "image/jpeg")}
    response = client.post("/api/v1/upload/", files=files)
    assert response.status_code == 401
