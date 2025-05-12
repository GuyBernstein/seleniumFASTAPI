from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_hello_endpoint():
    """Test the hello endpoint"""
    response = client.get("/hello")
    assert response.status_code == 200
    assert response.text == '"hello"'  # JSON string