from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_endpoint():
    response = client.post("/chat", json={"prompt": "سلام"})
    assert response.status_code == 200
    assert "response" in response.json()

def test_webhook_endpoint():
    response = client.post("/webhook", json={"prompt": "تست وب‌هوک"})
    assert response.status_code == 200
    assert len(response.json()["response"]) > 0