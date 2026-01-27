from typing import Optional
from openai import OpenAI


class OpenAIService:
    """Service for managing OpenAI API interactions."""

    def __init__(self, model: str, client: OpenAI):
        self.model = model
        self.client = client

    async def generate_response(
        self,
        messages: list,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 1000
    ) -> Optional[str]:
        """
        Generate a response from OpenAI based on messages and system prompt.
        """
        try:
            full_messages = [
                {"role": "system", "content": system_prompt},
                *messages
            ]

            response = self.client.chat.completions.create(
                model=self.model,
                messages=full_messages,
                temperature=temperature,
                max_tokens=max_tokens
            )

            return response.choices[0].message.content
        except Exception as e:
            print(f"OpenAI error: {e}")
            return None
