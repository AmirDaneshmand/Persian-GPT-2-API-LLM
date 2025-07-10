import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.parametrize("prompt,history", [
    ("سلام چطوری؟", ["سلام، خوبم"]),
    ("معنی زندگی چیست؟", ["زندگی چطور تعریف می‌شود؟"]),
    ("", [])  # تست ورودی خالی
])
def test_chat_endpoint(prompt, history):
    """تست endpoint چت با ورودی‌های مختلف و تاریخچه"""
    response = client.post(
        "/chat",
        json={
            "prompt": prompt,
            "history": history,
            "max_length": 50,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95
        }
    )
    
    if not prompt:
        assert response.status_code == 422  # Pydantic validation error
        assert "string_too_short" in response.json()["detail"][0]["type"]  # اصلاح نوع خطا
    else:
        assert response.status_code == 200
        assert "response" in response.json()
        assert "metrics" in response.json()
        assert response.json()["metrics"]["prompt_tokens"] > 0
        assert response.json()["metrics"]["generated_tokens"] > 0
        # بررسی اینکه تاریخچه در پاسخ تاثیر دارد
        if history:
            assert len(response.json()["response"]) > len(prompt)

def test_invalid_parameters():
    """تست پارامترهای نامعتبر"""
    response = client.post(
        "/chat",
        json={
            "prompt": "تست",
            "history": [],
            "temperature": 2.0,  # خارج از محدوده
            "max_length": 50,
            "top_k": 50,
            "top_p": 0.95
        }
    )
    assert response.status_code == 422  # Unprocessable Entity
    assert "temperature" in response.json()["detail"][0]["loc"]

def test_health_check():
    """تست endpoint سلامت سرویس"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

@pytest.mark.parametrize("invalid_max_length", [-1, 0, 1025])
def test_invalid_max_length(invalid_max_length):
    """تست مقادیر نامعتبر max_length"""
    response = client.post(
        "/chat",
        json={
            "prompt": "تست",
            "history": [],
            "max_length": invalid_max_length,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95
        }
    )
    assert response.status_code == 422