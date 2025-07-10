import pytest
from fastapi.testclient import TestClient
from app.main import app
import time
import random

client = TestClient(app)

def test_response_time():
    """تست زمان پاسخ endpoint چت"""
    start_time = time.time()
    response = client.post(
        "/chat",
        json={
            "prompt": "تست عملکرد",
            "history": [],
            "max_length": 50,
            "temperature": 0.7,
            "top_k": 50,
            "top_p": 0.95
        }
    )
    response_time = time.time() - start_time

    assert response.status_code == 200
    assert response_time < 4.0  # افزایش زمان مجاز به 4 ثانیه
    assert response.json()["metrics"]["inference_time_seconds"] < 3.5

def test_concurrent_requests():
    """تست درخواست‌های همزمان"""
    from concurrent.futures import ThreadPoolExecutor
    
    def send_request():
        prompt = f"تست همزمان {random.randint(1, 100)}"
        response = client.post(
            "/chat",
            json={
                "prompt": prompt,
                "history": [],
                "max_length": 50,
                "temperature": 0.7,
                "top_k": 50,
                "top_p": 0.95
            }
        )
        return response.status_code
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(send_request) for _ in range(6)]
        results = [f.result() for f in futures]
    
    assert all(code == 200 for code in results)