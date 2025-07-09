from pydantic import BaseModel
from pydantic import Field, confloat, validator
from typing import List


class ChatRequest(BaseModel):
    # prompt: str
    # history: List[str] = []  # اینجا لیست پیام‌های قبلی رو اضافه کردیم
    # max_length: int = Field(default=100, gt=0, le=500)
    # temperature: confloat(gt=0, le=1) = Field(default=0.7)
    # top_k: int = Field(default=50, gt=0)
    # top_p: float = Field(default=0.95)
    
    prompt: str = Field(..., min_length=1, description="متن پرسش یا پیام برای مدل")
    max_length: int = Field(100, ge=1, le=1024, description="حداکثر تعداد توکن تولید شده")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="دمای نمونه‌گیری")
    top_k: int = Field(50, ge=0, description="پارامتر top_k")
    top_p: float = Field(0.95, ge=0.0, le=1.0, description="پارامتر top_p")

class ChatResponse(BaseModel):
    response: str
    metrics: dict
# class ChatRequest(BaseModel):
#     prompt: str = Field(..., min_length=1, description="متن پرسش یا پیام برای مدل")
#     max_length: int = Field(100, ge=1, le=1024, description="حداکثر تعداد توکن تولید شده")
#     temperature: float = Field(0.7, ge=0.0, le=1.0, description="دمای نمونه‌گیری")
#     top_k: int = Field(50, ge=0, description="پارامتر top_k")
#     top_p: float = Field(0.95, ge=0.0, le=1.0, description="پارامتر top_p")

#     # اگر بخواهی اعتبارسنجی اضافه کنی:
#     @validator("prompt")
#     def prompt_not_empty(cls, v):
#         if not v.strip():
#             raise ValueError("prompt نباید خالی باشد")
#         return v