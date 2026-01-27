from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from services.knowledge import knowledge_texts
from services.openai_client import call_openai

router = Router()

def build_context(question: str) -> str:
    q = question.lower()
    parts = [knowledge_texts.get("about_andrey", "")]
    
    # План и стратегия
    if any(w in q for w in ["план", "стратег", "развити", "бренд", "канал"]):
        parts.append(knowledge_texts.get("brand_strategy", ""))
        parts.append(knowledge_texts.get("content_plan", ""))
    
    # Советы и питание
    if any(w in q for w in ["совет", "питан", "еда", "экипиров", "кроссовк", "техник"]):
        parts.append(knowledge_texts.get("running_tips", ""))
    
    # Новички
    if any(w in q for w in ["начать", "нович", "перв", "страшно"]):
        parts.append(knowledge_texts.get("beginner_support", ""))
        parts.append(knowledge_texts.get("easy_running_philosophy", ""))
    
    # Сообщество
    if any(w in q for w in ["сообществ", "группа", "совместн", "пробежк", "клуб"]):
        parts.append(knowledge_texts.get("community_and_runs", ""))
    
    return "\n\n---\n\n".join(p for p in parts if p)  # Обычные \n для промпта!

@router.message(Command("ask"))
async def ask(message: types.Message, command: CommandObject):
    question = command.args or ""
    if not question.strip():
        await message.answer(
            "❓ Напиши вопрос после команды, например:\\n"
            "/ask С чего начать бег после 30?"
        )
        return
    
    context = build_context(question)
    system_prompt = (
        "Ты — Андрей Потапов, автор канала про спокойный бег и сообщество.\\n"
        "Отвечай коротко, по делу, без планов тренировок и без медицинских советов.\\n"
        "Опирайся на базу знаний ниже, не противоречь им.\\n"
        "Если вопрос медицинский или про детальный план, мягко посоветуй обратиться к врачу или тренеру.\\n"
        "База знаний:\\n" + context
    )
    user_prompt = (
        f"Вопрос пользователя: {question}\\n"
        "Дай один связный ответ для Telegram."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="MarkdownV2")
