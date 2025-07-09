from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import PersianGPT2Model
from app.schemas import ChatRequest, ChatResponse
import os
from fastapi.responses import FileResponse

app = FastAPI(
    title="Persian GPT-2 API",
    description="API for local Persian GPT-2 model",
    version="1.0.0"
)

# تنظیم CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# مسیر مدل
current_dir = os.getcwd()
MODEL_PATH = f"{current_dir}/models/gpt2-fa"

# بارگذاری مدل
model = PersianGPT2Model(MODEL_PATH)

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400,
            detail="Prompt cannot be empty"
        )
    """Endpoint برای چت با مدل"""
    try:
        generation_params = {
            'max_length': request.max_length,
            'temperature': request.temperature,
            'top_k': request.top_k,
            'top_p': request.top_p
        }
        
        result = model.generate_text(request.prompt, generation_params)
        
        return {
            "response": result["generated_text"],
            "metrics": result["metrics"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/webhook")
async def webhook_endpoint(request: dict):
    """Endpoint برای وب‌هوک"""
    try:
        # پردازش درخواست وب‌هوک (با توجه به ساختار خاص وب‌هوک شما)
        prompt = request.get("prompt", "")
        if not prompt:
            return {"error": "Prompt is required"}
        
        result = model.generate_text(prompt)
        
        return {
            "response": result["generated_text"],
            "metrics": result["metrics"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """بررسی سلامت سرویس"""
    return {"status": "healthy"}


@app.get("/")
async def home():
    return {"message": "خوش آمدید به مدل LLM فارسی"}



@app.get('/favicon.ico', include_in_schema=False)
async def get_favicon():
    # مسیر به یک فایل favicon.ico (می‌توانید یک فایل ایجاد کنید یا از این استفاده کنید)
    favicon_path = os.path.join(os.path.dirname(__file__), "favicon.ico")
    return FileResponse(favicon_path)