import logging
from aiogram import Router, F
from aiogram.types import Message

from config import (
    SYSTEM_PROMPT_DEFAULT,
    SYSTEM_PROMPT_PLAN,
    SYSTEM_PROMPT_CONTENT,
    SYSTEM_PROMPT_AI_BOT
)
from services.openai_client import OpenAIService
from services.memory import MemoryService
from main import openai_service, memory_service

logger = logging.getLogger(__name__)
router = Router()


@router.message(F.text)
async def handle_message(message: Message):
    """Handle regular text messages."""
    try:
        user_id = message.from_user.id
        user_text = message.text

        # Determine mode based on context
        # For now, use default prompt
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
            await message.answer(
                "Ошибка при генерировании ответа. Попытайтесь ещё."
            )
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        await message.answer(
            "Ошибка сервера. Пожалуйста, попытайтесь позже."
        )
