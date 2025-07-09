from pydantic import BaseModel
from pydantic import Field, confloat

class ChatRequest(BaseModel):
    prompt: str
    max_length: int = Field(default=100, gt=0, le=500)
    temperature: confloat(gt=0, le=1) = Field(default=0.7)  # محدودیت 0-1
    top_k: int = Field(default=50, gt=0)
    top_p: float = 0.95

class ChatResponse(BaseModel):
    response: str
    metrics: dict