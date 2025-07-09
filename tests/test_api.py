import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("prompt,expected_length", [
    ("سلام چطوری؟", 10),
    ("معنی زندگی چیست؟", 15),
    ("", 0)  # تست ورودی خالی
])
def test_chat_endpoint(prompt, expected_length):
    """تست endpoint چت با ورودی‌های مختلف"""
    response = client.post(
        "/chat",
        json={"prompt": prompt, "max_length": 50}
    )
    
    if not prompt:  # برای ورودی خالی
        assert response.status_code == 400
    else:
        assert response.status_code == 200
        assert len(response.json()["response"].split()) >= expected_length


def test_invalid_parameters():
    """تست پارامترهای نامعتبر"""
    response = client.post(
        "/chat",
        json={"prompt": "test", "temperature": 2.0}  # temperature باید بین 0 و 1 باشد
    )
    assert response.status_code == 422  # Unprocessable Entity

def test_health_check():
    """تست endpoint سلامت سرویس"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_empty_prompt():
    """تست رفتار با prompt خالی"""
    response = client.post("/chat", json={"prompt": "", "max_length": 50})
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.parametrize("invalid_temp", [-1, 0, 1.1, 2])
def test_invalid_temperature(invalid_temp):
    """تست مقادیر نامعتبر temperature"""
    response = client.post(
        "/chat",
        json={"prompt": "test", "temperature": invalid_temp}
    )
    assert response.status_code == 422