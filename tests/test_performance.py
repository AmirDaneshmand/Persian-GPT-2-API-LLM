import pytest
from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_response_time():
    """تست زمان پاسخ endpoint چت"""
    start_time = time.time()
    response = client.post(
        "/chat",
        json={"prompt": "تست عملکرد", "max_length": 100}
    )
    response_time = time.time() - start_time
    
    assert response.status_code == 200
    assert response_time < 2.0  # پاسخ باید در کمتر از 2 ثانیه
    
    metrics = response.json()["metrics"]
    assert metrics["inference_time_seconds"] < 1.5

def test_concurrent_requests():
    """تست درخواست‌های همزمان"""
    from concurrent.futures import ThreadPoolExecutor
    import random
    
    def send_request():
        prompt = f"تست همزمان {random.randint(1, 100)}"
        response = client.post("/chat", json={"prompt": prompt, "max_length": 50})
        return response.status_code
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(send_request) for _ in range(10)]
        results = [f.result() for f in futures]
    
    assert all(code == 200 for code in results)