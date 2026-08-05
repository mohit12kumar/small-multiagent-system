import json
import os
from typing import Dict, Any
from groq import Groq
from backend.config import settings

def get_groq_client() -> Groq:
    api_key = settings.GROQ_API_KEY or os.getenv("GROQ_API_KEY", "")
    return Groq(api_key=api_key)

def query_groq_json(system_prompt: str, user_content: str, max_retries: int = 3) -> Dict[str, Any]:
    """
    Sends prompt to Groq API and expects a JSON formatted response, with retry handling for 429 Rate Limits.
    """
    client = get_groq_client()
    
    for attempt in range(max_retries + 1):
        try:
            response = client.chat.completions.create(
                model=settings.GROQ_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            content = response.choices[0].message.content
            return json.loads(content)
        except Exception as e:
            err_str = str(e)
            if ("429" in err_str or "rate_limit" in err_str.lower()) and attempt < max_retries:
                import time
                wait_time = 3.0 * (attempt + 1)
                print(f"[Groq Rate Limit]: Retrying in {wait_time}s (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(wait_time)
                continue
            print(f"[Groq Service Error]: {e}")
            return {"error": str(e)}
