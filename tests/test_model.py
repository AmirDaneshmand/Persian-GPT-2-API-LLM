import pytest
from app.models import PersianGPT2Model
import os

@pytest.fixture
def model():
    """فیکسچر مدل برای تست"""
    model_path = os.path.join(os.path.dirname(__file__), "../models/gpt2-fa")
    return PersianGPT2Model(model_path)

def test_model_generation(model):
    """تست تولید متن مدل"""
    result = model.generate_text("سلام")
    assert isinstance(result, dict)
    assert "generated_text" in result
    assert len(result["generated_text"]) > 10

def test_model_metrics(model):
    """تست معیارهای مدل"""
    result = model.generate_text("تست معیارها")
    metrics = result["metrics"]
    
    assert metrics["prompt_tokens"] > 0
    assert metrics["generated_tokens"] > 0
    assert metrics["tokens_per_second"] > 0