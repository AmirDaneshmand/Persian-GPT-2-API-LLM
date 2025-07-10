from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch
import time
from typing import Dict, Any
import os
import json
import logging
from datetime import datetime, UTC
from fastapi import HTTPException

# تنظیم logging
logging.basicConfig(
    filename="logs/app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class PersianGPT2Model:
    def __init__(self, model_path: str):
        self.model_path = model_path
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self.load_model()
    
    def load_model(self):
        """بارگذاری مدل و توکنایزر"""
        try:
            self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_path)
            self.model = GPT2LMHeadModel.from_pretrained(self.model_path)
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.model.config.pad_token_id = self.tokenizer.eos_token_id
            self.model = self.model.to(self.device)
            logging.info(f"Model loaded on {self.device}")
        except Exception as e:
            logging.error(f"Error loading model: {str(e)}")
            raise
        
    def generate_text(self, prompt: str, generation_params: Dict[str, Any] = None) -> Dict[str, Any]:
        """تولید متن با ثبت معیارهای عملکرد"""
        default_params = {
            'max_length': 100,
            'do_sample': True,
            'temperature': 0.7,
            'top_k': 50,
            'top_p': 0.95,
            'no_repeat_ngram_size': 3,
            'repetition_penalty': 1.5,
            'num_beams': 3,
            'early_stopping': True
        }
        
        if generation_params is not None:
            default_params.update(generation_params)
        generation_params = default_params
        
        # زمان شروع
        start_time = time.time()
        
        try:
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
                no_repeat_ngram_size=generation_params.get("no_repeat_ngram_size", 3),
                repetition_penalty=generation_params.get("repetition_penalty", 1.5),
                num_beams=generation_params.get("num_beams", 3),
                early_stopping=generation_params.get("early_stopping", True),
                pad_token_id=self.tokenizer.eos_token_id,
                do_sample=generation_params.get("do_sample", True)
            )
            
            # دیکد خروجی
            generated_text = self.tokenizer.decode(output_ids[0], skip_special_tokens=True)
            
            # محاسبه معیارهای عملکرد
            inference_time = time.time() - start_time
            prompt_tokens = inputs["input_ids"].shape[1]
            generated_tokens = output_ids.shape[1] - prompt_tokens
            tokens_per_second = generated_tokens / inference_time if inference_time > 0 else 0
            
            metrics = {
                "generated_text": generated_text,
                "metrics": {
                    "inference_time_seconds": inference_time,
                    "prompt_tokens": prompt_tokens,
                    "generated_tokens": generated_tokens,
                    "tokens_per_second": tokens_per_second,
                    "total_tokens": prompt_tokens + generated_tokens,
                    "device": str(self.device)
                }
            }
            
            log_metrics(metrics)
            return metrics
            
        except torch.cuda.OutOfMemoryError:
            logging.error("GPU memory exceeded")
            raise HTTPException(status_code=500, detail="GPU memory exceeded")
        except Exception as e:
            logging.error(f"Error generating text: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Model error: {str(e)}")
    
def log_metrics(metrics):
    """ذخیره معیارهای عملکرد در لاگ"""
    log_entry = {
        "timestamp": datetime.now(UTC).isoformat(),
        **metrics
    }
    logging.info(json.dumps(log_entry, ensure_ascii=False))