from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Handle /start command."""
    await message.answer(
        "👋 Привет! Я — личный ассистент Андрея Потапова.\\n"
        "\\n📝 *Генерация постов:*\\n"
        "/post_easy - пост про спокойный бег\\n"
        "/post_beginner - поддержка новичков\\n"
        "/post_community - про сообщество\\n"
        "/post_about - пост-знакомство\\n\\n"
        "❓ *Вопросы-ответы:*\\n"
        "/ask [вопрос] - ответь на вопрос о беге\\n\\n"
        "⚙️ *Другое:*\\n"
        "/ai_bot_help - помощь с AI-ботами\\n"
        "/help - справка",
        parse_mode="MarkdownV2"  # ← V2 обязательно!
    )

@router.message(Command("ai_bot_help"))
async def cmd_ai_help(message: Message):
    """Handle /ai_bot_help command."""
    await message.answer(
        "🤖 Режим помощи с AI-ботами.\\n"
        "Какой вопрос у тебя по OpenAI, Claude или автоматизации?"
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Handle /help command."""
    await message.answer(
        "📚 *Доступные команды:*\\n\\n"
        "📝 *Генерация постов:*\\n"
        "/post_easy - пост про спокойный бег\\n"
        "/post_beginner - поддержка новичков\\n"
        "/post_community - про сообщество\\n"
        "/post_about - пост-знакомство\\n\\n"
        "❓ *Вопросы-ответы:*\\n"
        "/ask [вопрос] - ответь на вопрос о беге\\n\\n"
        "⚙️ *Другое:*\\n"
        "/ai_bot_help - помощь с AI-ботами\\n"
        "/help - эта справка",
        parse_mode="MarkdownV2"  # ← V2 обязательно!
    )
