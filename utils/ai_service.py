"""
AI service helpers for summarization and document Q&A.
Uses an OpenAI-compatible HTTP call when OPENAI_API_KEY is configured.
"""

import os
import requests


OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
REQUEST_TIMEOUT = 45


def is_configured():
    return bool(os.getenv("OPENAI_API_KEY"))


def ask_ai(system_prompt, user_prompt, max_tokens=300):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return None

    response = requests.post(
        OPENAI_API_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        json={
            "model": DEFAULT_MODEL,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "temperature": 0.2,
            "max_tokens": max_tokens
        },
        timeout=REQUEST_TIMEOUT
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
