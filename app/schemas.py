from pydantic import BaseModel
from pydantic import Field
from typing import List

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1, description="متن پرسش یا پیام برای مدل")
    history: List[str] = Field(default_factory=list, description="تاریخچه پیام‌های قبلی")
    max_length: int = Field(100, ge=1, le=1024, description="حداکثر تعداد توکن تولید شده")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="دمای نمونه‌گیری")
    top_k: int = Field(50, ge=0, description="پارامتر top_k")
    top_p: float = Field(0.95, ge=0.0, le=1.0, description="پارامتر top_p")

class ChatResponse(BaseModel):
    response: str
    metrics: dict