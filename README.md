Persian GPT-2 API
مقدمه
این پروژه یک API مبتنی بر FastAPI است که از مدل زبانی GPT-2 پارسی برای تولید متن استفاده می‌کند. API شامل دو endpoint اصلی (/chat و /webhook) است که امکان تعامل با مدل را با پشتیبانی از تاریخچه و context فراهم می‌کنند. پروژه با تست‌های جامع pytest بررسی شده و عملکرد آن روی CPU پایدار است.
ساختار پروژه

app/: شامل فایل‌های اصلی برنامه (main.py, schemas.py, models.py).
tests/: شامل تست‌های API، مدل، عملکرد، و وب‌هوک.
logs/: لاگ‌های برنامه در app.log.
models/gpt2-fa/: مدل GPT-2 پارسی.
requirements.txt: وابستگی‌های پروژه.

نصب و راه‌اندازی

نصب مدل:git clone https://huggingface.co/HooshvareLab/gpt2-fa models/gpt2-fa

نصب وابستگی‌ها:pip install -r requirements.txt

غیرفعال کردن پیام‌های TensorFlow:export TF_ENABLE_ONEDNN_OPTS=0 # لینوکس/مک
set TF_ENABLE_ONEDNN_OPTS=0 # ویندوز

اجرای سرور:uvicorn app.main:app --host 0.0.0.0 --port 8000

اجرای تست‌ها:pytest tests/ -v

API Endpointها

GET /: پیام خوش‌آمدگویی.
پاسخ: {"message": "خوش آمدید به مدل LLM فارسی"}

GET /health: بررسی سلامت سرویس.
پاسخ: {"status": "healthy"}

POST /chat: تولید متن با تاریخچه.
ورودی: {"prompt": "string", "history": ["string"], "max_length": int, "temperature": float, "top_k": int, "top_p": float}
مثال:curl -X POST "http://localhost:8000/chat" -H "Content-Type: application/json" -d '{"prompt": "اسم من چیست؟", "history": ["سلام، من علی هستم"], "max_length": 20, "temperature": 0.7, "top_k": 50, "top_p": 0.95}'

POST /webhook: وب‌هوک برای سیستم‌های خارجی.
ورودی: {"prompt": "string", "context": {"user_id": "string", "history": ["string"], "project": "string"}, "options": {"max_length": int, "format": "string"}}
مثال:curl -X POST "http://localhost:8000/webhook" -H "Content-Type: application/json" -d '{"prompt": "اسم من چیست؟", "context": {"user_id": 123, "history": ["سلام، من سارا هستم"]}, "options": {"max_length": 20}}'

تست‌ها

18 تست در 4 فایل (test_api.py, test_model.py, test_performance.py, test_webhook.py) با موفقیت اجرا شده‌اند.
برای اجرا:pytest tests/ -v

معیارهای عملکرد

معیارها (زمان استنتاج، تعداد توکن‌ها، توکن بر ثانیه) در logs/app.log ثبت می‌شوند.
زمان استنتاج روی CPU حدود 4-4.5 ثانیه برای max_length=30.

بهینه‌سازی‌های پیشنهادی

کاهش max_length: به 20 برای کاهش زمان استنتاج.
استفاده از GPU: نصب torch با پشتیبانی CUDA.
Mixed-Precision: استفاده از torch.cuda.amp.autocast برای بهبود عملکرد روی GPU.
