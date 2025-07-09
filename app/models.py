from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
from typing import Dict, Any
import os
import json
from datetime import datetime

class PersianGPT2Model:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.load_model()
        
    def load_model(self):
        """بارگذاری مدل و توکنایزر"""
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
        self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
        
        # تنظیم توکن پد
        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.model.config.pad_token_id = self.tokenizer.eos_token_id
        
        # انتقال مدل به دستگاه (GPU/CPU)
        self.model = self.model.to(self.device)
    
    def generate_text(self, prompt: str, generation_params: Dict[str, Any] = None) -> Dict[str, Any]:
        if generation_params is None:
            generation_params = {
                'max_length': 100,
                'do_sample': True,
                # 'top_k': 50,
                'top_k': 40,
                # 'top_p': 0.95,
                'top_p': 0.9,
                # 'temperature': 0.8,
                'temperature': 0.6,
                # 'num_beams': 1,  # کاهش از 4 به 1 برای سرعت بیشتر
                'num_beams': 3,
                'early_stopping': True,
                'no_repeat_ngram_size': 2
            }
        """تولید متن با ثبت معیارهای عملکرد"""
        if generation_params is None:
            generation_params = {
                # 'max_length': 100,
                # 'do_sample': True,
                # 'top_k': 50,
                # 'top_p': 0.95,
                # 'temperature': 0.8
                'max_length': 100,
                'do_sample': False,           # نمونه برداری خاموش
                'num_beams': 5,               # beam search قوی‌تر
                'early_stopping': True,
                'no_repeat_ngram_size': 4,    # جلوگیری از تکرار n-gram طولانی‌تر
                'temperature': 1.0,           # یا حذف شود
                'top_k': 0,                   # با beam search بهتر است روی 0 تنظیم شود
                'top_p': 0.0                  # با beam search بهتر است روی 0 تنظیم شود
            }
        
        # زمان شروع
        start_time = time.time()
        
        # توکنایز ورودی
        inputs = self.tokenizer(prompt, return_tensors="pt", padding=True, truncation=True, max_length=512)
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # تولید متن
        output_ids = self.model.generate(
            **inputs,
            max_new_tokens=generation_params.get("max_length", 100),
            temperature=generation_params.get("temperature", 0.7),
            top_k=generation_params.get("top_k", 50),
            top_p=generation_params.get("top_p", 0.95),
            pad_token_id=self.tokenizer.eos_token_id,
            
            no_repeat_ngram_size=3,  # جلوگیری از تکرار
            repetition_penalty=1.5,  # جریمه برای تکرار
            do_sample=True,
            early_stopping=True
        )
        
        # دیکد خروجی
        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        # محاسبه معیارهای عملکرد
        inference_time = time.time() - start_time
        prompt_tokens = inputs["input_ids"].shape[1]
        generated_tokens = output_ids.shape[1] - prompt_tokens
        tokens_per_second = generated_tokens / inference_time
        
        metrics = {
            "generated_text": generated_text,
            "metrics": {
                "inference_time_seconds": inference_time,
                "prompt_tokens": prompt_tokens,
                "generated_tokens": generated_tokens,
                "tokens_per_second": tokens_per_second,
                "total_tokens": prompt_tokens + generated_tokens
            }
        }

        log_metrics(metrics)

        return metrics
    
def log_metrics(metrics):
    
    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **metrics
    }

    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "metrics_log.json")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")



    
