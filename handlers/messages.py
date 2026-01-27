import logging
from aiogram import Router, F
from aiogram.types import Message
from openai import AsyncOpenAI

from config import (
    SYSTEM_PROMPT_DEFAULT,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    MAX_HISTORY_LENGTH
)
from services.openai_client import OpenAIService
from services.memory import MemoryService

logger = logging.getLogger(__name__)
router = Router()

# Initialize services locally (singleton pattern)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
openai_service = OpenAIService(model=OPENAI_MODEL, client=openai_client)
memory_service = MemoryService(max_history=MAX_HISTORY_LENGTH)

@router.message(F.text)
async def handle_message(message: Message):
    """Handle regular text messages."""
    try:
        user_id = message.from_user.id
        user_text = message.text

        # Skip commands (handled by other routers)
        if user_text.startswith('/'):
            return

        # Determine mode based on context (TODO: implement modes)
        system_prompt = SYSTEM_PROMPT_DEFAULT

        # Add user message to history
        memory_service.add_message(user_id, "user", user_text)

        # Get conversation history
        history = memory_service.get_history(user_id)

        # Generate response
        response = await openai_service.generate_response(
            messages=history,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )

        if response:
            # Add assistant response to history
            memory_service.add_message(user_id, "assistant", response)
            await message.answer(response)
        else:
            await message.answer("❌ Ошибка при генерации ответа. Попробуйте ещё раз.")
            
    except Exception as e:
        logger.error(f"Error handling message {message.from_user.id}: {e}", exc_info=True)
        await message.answer("❌ Серверная ошибка. Попробуйте позже.")
