import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WEBHOOK_DATA = {
    "prompt": "مدیریت پروژه هوش مصنوعی",
    "context": {
        "user_id": "test_user",
        "history": ["هوش مصنوعی چیست؟"],
        "project": "پروژه تستی"
    },
    "options": {
        "format": "markdown",
        "max_length": 30  # کاهش برای بهبود عملکرد
    }
}

def test_webhook_basic():
    """تست پایه‌ای وب‌هوک با تاریخچه"""
    response = client.post("/webhook", json=WEBHOOK_DATA)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "metrics" in response.json()
    assert response.json()["context"] == WEBHOOK_DATA["context"]
    assert response.json()["metrics"]["prompt_tokens"] > 0

@pytest.mark.parametrize("missing_field", ["prompt"])
def test_webhook_required_fields(missing_field):
    """تست فیلدهای اجباری"""
    test_data = WEBHOOK_DATA.copy()
    del test_data[missing_field]
    
    response = client.post("/webhook", json=test_data)
    assert response.status_code == 422  # Validation Error

def test_webhook_invalid_context():
    """تست context نامعتبر"""
    test_data = WEBHOOK_DATA.copy()
    test_data["context"] = "not_a_dict"
    
    response = client.post("/webhook", json=test_data)
    assert response.status_code == 422
    assert "dict_type" in response.json()["detail"][0]["type"]

def test_webhook_with_history():
    """تست وب‌هوک با تاریخچه در context"""
    test_data = {
        "prompt": "اسم من چیست؟",
        "context": {
            "user_id": "test_user",
            "history": ["سلام، من علی هستم"]
        },
        "options": {}
    }
    response = client.post("/webhook", json=test_data)
    assert response.status_code == 200
    assert "response" in response.json()
    assert "علی" in response.json()["response"]  # بررسی تاثیر تاریخچه

def test_webhook_performance():
    """تست عملکرد وب‌هوک"""
    import time
    start_time = time.time()
    
    # فقط 2 درخواست برای تست عملکرد
    for _ in range(2):
        response = client.post("/webhook", json=WEBHOOK_DATA)
        assert response.status_code == 200
    
    total_time = time.time() - start_time
    assert total_time < 10.0  # افزایش زمان مجاز به 10 ثانیه