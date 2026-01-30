from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import (
    SYSTEM_PROMPT_CONTENT,
    OPENAI_MODEL,
    OPENAI_API_KEY,
    MAX_HISTORY_LENGTH,
)
from openai import AsyncOpenAI
from services.openai_client import OpenAIService
from services.memory import MemoryService

router = Router()

# Инициализируем сервисы (как в messages.py)
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)
openai_service = OpenAIService(model=OPENAI_MODEL, client=openai_client)
memory_service = MemoryService(max_history=MAX_HISTORY_LENGTH)

@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "👋 Привет! Я — личный ассистент Андрея Потапова.\n\n"
        "Главное: пиши вопросы текстом без слэша — я отвечу как личный ассистент.\n\n"
        "Команды:\n"
        "/help – список возможностей\n"
        "/ai_bot_help – режим про AI-ботов\n"
        "/post_easy, /post_beginner, /post_community, /post_about – сгенерировать посты."
    )
    await message.answer(text)

@router.message(Command("ai_bot_help"))
async def cmd_ai_help(message: Message):
    await message.answer(
        "🤖 Режим помощи с AI-ботами.\n"
        "Задай вопрос про OpenAI, Claude, Telegram-ботов или автоматизацию контента."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    text = (
        "📚 Что я умею:\n\n"
        "1) Бег и тренировки\n"
        "2) Контент и посты\n"
        "3) AI-боты и автоматизация\n\n"
        "Команды:\n"
        "/start – краткая инструкция\n"
        "/ai_bot_help – режим про AI-ботов\n"
        "/post_easy – пост про спокойный бег\n"
        "/post_beginner – пост для новичков\n"
        "/post_community – пост про сообщество\n"
        "/post_about – пост-знакомство\n\n"
        "А главное — просто пиши вопросы текстом, без слэша."
    )
    await message.answer(text)

# ----- Команды-посты через ChatGPT -----

async def _generate_post(message: Message, topic_instruction: str):
    """Общий помощник для генерации постов."""
    user_id = message.from_user.id

    system_prompt = SYSTEM_PROMPT_CONTENT
    user_prompt = (
        f"Сгенерируй один связный пост для Telegram на тему:\n{topic_instruction}\n\n"
        "Стиль: живой, понятный, без воды. 150–250 слов."
    )

    # История для конкретного юзера (можно не использовать, если не нужно)
    memory_service.add_message(user_id, "user", user_prompt)
    history = memory_service.get_history(user_id)

    response = await openai_service.generate_response(
        messages=history,
        system_prompt=system_prompt,
        temperature=0.8,
        max_tokens=800,
    )

    if response:
        memory_service.add_message(user_id, "assistant", response)
        await message.answer(response)
    else:
        await message.answer("❌ Не удалось сгенерировать пост, попробуй ещё раз.")

@router.message(Command("post_easy"))
async def cmd_post_easy(message: Message):
    await _generate_post(
        message,
        "спокойный лёгкий бег для любителя 30–45 лет, зачем он нужен и как его делать",
    )

@router.message(Command("post_beginner"))
async def cmd_post_beginner(message: Message):
    await _generate_post(
        message,
        "поддержка новичка в беге: как начать, не перегореть и не травмироваться",
    )

@router.message(Command("post_community"))
async def cmd_post_community(message: Message):
    await _generate_post(
        message,
        "ценность бегового сообщества и совместных тренировок, пример твоего коммьюнити",
    )

@router.message(Command("post_about"))
async def cmd_post_about(message: Message):
    await _generate_post(
        message,
        "пост-знакомство от лица Андрея Потапова: кто ты, как бежишь, зачем тебе бег и AI",
    )
