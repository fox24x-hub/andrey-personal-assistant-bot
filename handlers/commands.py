from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(
        "Привет, это личный ассистент Андрея Потапова!\n"
        "Выбери режим:\n"
        "/content - идеи контента\n"
        "/ai_bot_help - помощь с AI-ботами\n"
        "Или просто пиши вопрос!"
    )


@router.message(Command("content"))
async def cmd_content(message: Message):
    """Handle /content command."""
    await message.answer(
        "Режим создания контента.\n"
        "Какую идею контента ты хочешь развить?"
    )


@router.message(Command("ai_bot_help"))
async def cmd_ai_help(message: Message):
    """Handle /ai_bot_help command."""
    await message.answer(
        "Режим помощи с AI-ботами.\n"
        "Какой вопрос у тебя по OpenAI, Claude или автоматизации?"
    )


@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(
        "Доступные команды:\n"
        "/start - начать\n"
        "/content - контент\n"
        "/ai_bot_help - AI-ботов\n"
        "/help - эта справка"
    )
