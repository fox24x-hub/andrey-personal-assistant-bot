import os
from typing import List, Dict, Any

from openai import AsyncOpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")



_default_client = AsyncOpenAI(api_key=OPENAI_API_KEY)\n

class OpenAIService:   
    def __init__(self, model: str = OPENAI_MODEL, client: AsyncOpenAI | None = None):
        self.model = model
        self.client = client or AsyncOpenAI(api_key=OPENAI_API_KEY)

    async def generate_response(
        self,
        messages: List[Dict[str, Any]],
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000,
    ) -> str | None:
        """
        Основной метод, который использует handlers/messages.py:
        берёт history + system_prompt и возвращает текст.
        """
        full_messages: List[Dict[str, str]] = [
            {"role": "system", "content": system_prompt},
            *messages,
        ]

        resp = await self.client.chat.completions.create(
            model=self.model,
            messages=full_messages,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        return resp.choices[0].message.content


async def call_openai(system_prompt: str, user_prompt: str) -> str:
    """
    Упрощённый вызов для knowledge-хэндлеров (/post_*, /ask).
    """
    resp = await client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.7,
        max_tokens=800,
    )
    return resp.choices[0].message.content or ""
