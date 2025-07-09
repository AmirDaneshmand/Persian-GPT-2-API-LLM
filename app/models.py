from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
from typing import Dict, Any
import os

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
            generation_params = {}
        """تولید متن با ثبت معیارهای عملکرد"""
        if generation_params is None:
            generation_params = {
                'max_length': 100,
                'do_sample': True,
                'top_k': 50,
                'top_p': 0.95,
                'temperature': 0.8
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
            pad_token_id=self.tokenizer.eos_token_id
        )
        
        # دیکد خروجی
        generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
        
        # محاسبه معیارهای عملکرد
        inference_time = time.time() - start_time
        prompt_tokens = inputs["input_ids"].shape[1]
        generated_tokens = output_ids.shape[1] - prompt_tokens
        tokens_per_second = generated_tokens / inference_time
        
        return {
            "generated_text": generated_text,
            "metrics": {
                "inference_time_seconds": inference_time,
                "prompt_tokens": prompt_tokens,
                "generated_tokens": generated_tokens,
                "tokens_per_second": tokens_per_second,
                "total_tokens": prompt_tokens + generated_tokens
            }
        }