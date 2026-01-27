from aiogram import Router, types
from aiogram.filters import Command, CommandObject
from services.openai_client import call_openai
from services.knowledge import knowledge_texts

router = Router()

@router.message(Command("post_easy"))
async def post_easy(message: types.Message, command: CommandObject):
    kb = knowledge_texts.get("easy_running_philosophy", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост для личного ТГ-канала про спокойный бег.\n"
        "Опирайся на знания ниже, не противоречь им.\n"
        "Стиль: простой, человеческий, без тренерства, без планов тренировок.\n"
        "Текст из базы знаний:\n" + kb
    )
    user_prompt = (
        "Сгенерируй один связный пост для канала.\n"
        f"Фокус: {user_hint or 'объяснить, что такое спокойный бег для взрослых новичков.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")

@router.message(Command("post_beginner"))
async def post_beginner(message: types.Message, command: CommandObject):
    kb = knowledge_texts.get("beginner_support", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост для личного ТГ-канала про поддержку новичков.\n"
        "Опирайся на знания ниже, не противоречь им.\n"
        "Стиль: простой, поддерживающий, без медицины и без планов тренировок.\n"
        "Текст из базы знаний:\n" + kb
    )
    user_prompt = (
        "Сгенерируй один связный пост для канала.\n"
        f"Фокус: {user_hint or 'поддержка новичка, которому страшно начинать бег.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")

@router.message(Command("post_community"))
async def post_community(message: types.Message, command: CommandObject):
    kb = knowledge_texts.get("community_and_runs", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост про сообщество и совместные пробежки.\n"
        "Опирайся на знания ниже, не противоречь им.\n"
        "Стиль: простой, дружелюбный, без тренерства.\n"
        "Текст из базы знаний:\n" + kb
    )
    user_prompt = (
        "Сгенерируй один связный пост для канала.\n"
        f"Фокус: {user_hint or 'зачем вообще беговое сообщество взрослым людям.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")

@router.message(Command("post_about"))
async def post_about(message: types.Message, command: CommandObject):
    kb = knowledge_texts.get("about_andrey", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост-знакомство для личного канала.\n"
        "Опирайся на знания ниже, не противоречь им.\n"
        "Стиль: простой, честный, без пафоса.\n"
        "Текст из базы знаний:\n" + kb
    )
    user_prompt = (
        "Сгенерируй один связный пост-знакомство для канала.\n"
        f"Фокус: {user_hint or 'кто ты, чем занимаешься и почему тебе важен спокойный бег.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")

@router.message(Command("post_tips"))
async def post_tips(message: types.Message, command: CommandObject):
    kb = knowledge_texts.get("running_tips", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост с практическими советами для бегунов 30+.\n"
        "Опирайся на знания ниже (питание, экипировка, техника).\n"
        "Стиль: практичный, экспертный, но простой.\n"
        "Текст из базы знаний:\n" + kb
    )
    user_prompt = (
        "Сгенерируй пост с советами.\n"
        f"Фокус: {user_hint or 'питание и восстановление при офисной работе.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")

@router.message(Command("post_strategy"))
async def post_strategy(message: types.Message, command: CommandObject):
    kb_strat = knowledge_texts.get("brand_strategy", "")
    kb_plan = knowledge_texts.get("content_plan", "")
    user_hint = command.args
    system_prompt = (
        "Ты — Андрей Потапов. Пишешь пост, опираясь на свою стратегию развития и контент-план.\n"
        "Твоя миссия: бег для жизни, а не жизнь для бега.\n"
        "Текст стратегии и плана:\n" + kb_strat + "\n" + kb_plan
    )
    user_prompt = (
        "Сгенерируй пост для канала.\n"
        f"Фокус: {user_hint or 'почему я строю это сообщество и какая у нас миссия.'}\n"
        "Без эмодзи, 1–2 подзаголовка максимум."
    )
    answer = await call_openai(system_prompt, user_prompt)
    await message.answer(answer, parse_mode="Markdown")
