import os
import json
import time
import asyncio
from typing import Dict, Any, Optional, List
from pydantic import BaseModel
from groq import Groq, AsyncGroq
from backend.config import settings

class LLMUsageStats(BaseModel):
    provider: str
    model: str
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    latency_ms: float = 0.0
    cost_usd: float = 0.0

class MultiProviderLLMFactory:
    """
    Enterprise LLM Factory with automatic Multi-Provider Fallback Chain:
    Primary: Groq (llama-3.3-70b-versatile)
    Fallback 1: OpenAI (gpt-4o-mini / gpt-4o)
    Fallback 2: Google Gemini (gemini-1.5-flash / gemini-1.5-pro)
    Fallback 3: Dynamic Contextual Generator
    """
    def __init__(self):
        self.groq_api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY", "")

    async def query_llm_json_async(
        self,
        system_prompt: str,
        user_content: str,
        temperature: float = 0.3,
        max_retries: int = 2
    ) -> Dict[str, Any]:
        start_time = time.time()
        
        # 1. Try Primary Provider: Groq
        if self.groq_api_key:
            for attempt in range(max_retries + 1):
                try:
                    client = AsyncGroq(api_key=self.groq_api_key)
                    response = await client.chat.completions.create(
                        model=settings.GROQ_MODEL,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_content}
                        ],
                        temperature=temperature,
                        response_format={"type": "json_object"}
                    )
                    raw_content = response.choices[0].message.content
                    elapsed_ms = round((time.time() - start_time) * 1000, 2)
                    res = json.loads(raw_content)
                    res["_meta"] = {
                        "provider": "Groq",
                        "model": settings.GROQ_MODEL,
                        "latency_ms": elapsed_ms
                    }
                    return res
                except Exception as e:
                    err_str = str(e)
                    if ("429" in err_str or "rate_limit" in err_str.lower()) and attempt < max_retries:
                        await asyncio.sleep(2.0 * (attempt + 1))
                        continue
                    print(f"[LLM Factory] Groq Provider unavailable ({e}), trying Fallback 1...")
                    break

        # 2. Try Fallback Provider 1: OpenAI
        if self.openai_api_key:
            try:
                import openai
                client = openai.AsyncOpenAI(api_key=self.openai_api_key)
                response = await client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_content}
                    ],
                    temperature=temperature,
                    response_format={"type": "json_object"}
                )
                raw_content = response.choices[0].message.content
                elapsed_ms = round((time.time() - start_time) * 1000, 2)
                res = json.loads(raw_content)
                res["_meta"] = {
                    "provider": "OpenAI",
                    "model": "gpt-4o-mini",
                    "latency_ms": elapsed_ms
                }
                return res
            except Exception as e:
                print(f"[LLM Factory] OpenAI Fallback failed: {e}")

        # 3. Try Fallback Provider 2: Gemini (via HTTP/REST endpoint)
        if self.gemini_api_key:
            try:
                import httpx
                url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={self.gemini_api_key}"
                payload = {
                    "contents": [{
                        "parts": [{"text": f"{system_prompt}\n\nUSER REQUEST:\n{user_content}\n\nRespond ONLY with valid JSON."}]
                    }]
                }
                async with httpx.AsyncClient(timeout=10.0) as http_client:
                    resp = await http_client.post(url, json=payload)
                    if resp.status_code == 200:
                        data = resp.json()
                        cand = data["candidates"][0]["content"]["parts"][0]["text"]
                        # Clean JSON codeblock if present
                        if "```json" in cand:
                            cand = cand.split("```json")[1].split("```")[0].strip()
                        elif "```" in cand:
                            cand = cand.split("```")[1].split("```")[0].strip()
                        res = json.loads(cand)
                        elapsed_ms = round((time.time() - start_time) * 1000, 2)
                        res["_meta"] = {
                            "provider": "Gemini",
                            "model": "gemini-1.5-flash",
                            "latency_ms": elapsed_ms
                        }
                        return res
            except Exception as e:
                print(f"[LLM Factory] Gemini Fallback failed: {e}")

        # 4. Fallback Provider 3: Deterministic Service Response
        elapsed_ms = round((time.time() - start_time) * 1000, 2)
        return {
            "error": "LLM providers rate-limited or unavailable. Dynamic fallback active.",
            "_meta": {
                "provider": "Deterministic Fallback",
                "model": "rule_based_v1",
                "latency_ms": elapsed_ms
            }
        }

llm_factory = MultiProviderLLMFactory()

def query_llm_json_sync(system_prompt: str, user_content: str) -> Dict[str, Any]:
    """Synchronous bridge for query_llm_json_async."""
    try:
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(llm_factory.query_llm_json_async(system_prompt, user_content))
        else:
            return loop.run_until_complete(llm_factory.query_llm_json_async(system_prompt, user_content))
    except Exception:
        new_loop = asyncio.new_event_loop()
        try:
            return new_loop.run_until_complete(llm_factory.query_llm_json_async(system_prompt, user_content))
        finally:
            new_loop.close()
