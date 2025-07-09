import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

WEBHOOK_DATA = {
    "prompt": "مدیریت پروژه هوش مصنوعی",
    "context": {
        "user_id": "test_user",
        "project": "پروژه تستی"
    },
    "options": {
        "format": "markdown"
    }
}

def test_webhook_basic():
    """تست پایه‌ای وب‌هوک"""
    response = client.post("/webhook", json=WEBHOOK_DATA)
    assert response.status_code == 200
    assert "response" in response.json()
    assert len(response.json()["response"]) > 10

@pytest.mark.parametrize("missing_field", ["prompt"])
def test_webhook_required_fields(missing_field):
    """تست فیلدهای اجباری"""
    test_data = WEBHOOK_DATA.copy()
    del test_data[missing_field]
    
    response = client.post("/webhook", json=test_data)
    assert response.status_code == 422  # Validation Error

def test_webhook_performance():
    """تست عملکرد وب‌هوک"""
    import time
    start_time = time.time()
    
    # فقط 2 درخواست برای تست عملکرد
    for _ in range(2):
        response = client.post("/webhook", json=WEBHOOK_DATA)
        assert response.status_code == 200
    
    total_time = time.time() - start_time
    assert total_time < 6.0  # زمان معقول برای 2 درخواست