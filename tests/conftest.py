import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))  # اضافه کردن مسیر ریشه به sys.path

from app.main import app
@pytest.fixture
def test_client():
    """فیکسچر کلاینت تست"""
    return TestClient(app)

@pytest.fixture
def sample_prompts():
    """داده‌های تستی برای promptها"""
    return [
        "سلام دنیا",
        "چطور می‌توانم یک مدل زبانی بسازم؟",
        "معرفی کتاب برای یادگیری پایتون"
    ]