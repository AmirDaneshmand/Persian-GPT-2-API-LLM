import pytest
from fastapi.testclient import TestClient
import sys
import os
from pathlib import Path

# غیرفعال کردن پیام‌های oneDNN
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

sys.path.append(str(Path(__file__).parent.parent))  # اضافه کردن مسیر ریشه به sys.path
from app.main import app

@pytest.fixture(scope="session")
def client():
    """فیکسچر کلاینت برای تست‌ها"""
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_prompts():
    """داده‌های تستی برای promptها و تاریخچه"""
    return [
        {"prompt": "سلام دنیا", "history": []},
        {"prompt": "چطور می‌توانم یک مدل زبانی بسازم؟", "history": ["مدل‌های زبانی چیست؟"]},
        {"prompt": "معرفی کتاب برای یادگیری پایتون", "history": ["پایتون چیست؟", "چطور پایتون یاد بگیرم؟"]}
    ]