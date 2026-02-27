"""
Hugging Face Inference API Client for OpenCLAW Nebula-Engineer.
Optimized for Qwen2.5-72B-Instruct.
"""

import os
import httpx
import asyncio
import logging

logger = logging.getLogger(__name__)

HF_TOKEN = os.getenv("HF_TOKEN", "")
DEFAULT_MODEL = "Qwen/Qwen2.5-72B-Instruct"
BASE_URL = f"https://api-inference.huggingface.co/models/{DEFAULT_MODEL}/v1/chat/completions"

async def complete(
    messages: list,
    max_tokens: int = 4000,
    temperature: float = 0.7,
    fast: bool = False,
) -> str:
    if not HF_TOKEN:
        raise RuntimeError("HF_TOKEN not found in environment.")

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": DEFAULT_MODEL,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
        "stream": False
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        for attempt in range(3):
            try:
                r = await client.post(BASE_URL, headers=headers, json=payload)
                if r.status_code == 429:
                    await asyncio.sleep(20 * (attempt + 1))
                    continue
                r.raise_for_status()
                data = r.json()
                return data["choices"][0]["message"]["content"].strip()
            except Exception as e:
                if attempt == 2:
                    raise RuntimeError(f"HF Inference API failed: {e}")
                await asyncio.sleep(5 * (attempt + 1))

    raise RuntimeError("HF Inference: retries exhausted")
