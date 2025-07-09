import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # اضافه کردن مسیر ریشه به sys.path
from app.main import app



@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_prompts():
    """داده‌های تستی برای promptها"""
    return [
        "سلام دنیا",
        "چطور می‌توانم یک مدل زبانی بسازم؟",
        "معرفی کتاب برای یادگیری پایتون"
    ]


