import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_HOST = os.getenv("WEBHOOK_HOST", "localhost")
WEBHOOK_PORT = int(os.getenv("WEBHOOK_PORT", 8000))

# OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o")

# System prompts
SYSTEM_PROMPT_DEFAULT = """
Ты личный ассистент Андрея Потапова по бегу, AI-ботам и контенту.
Отвечай кратко, по делу, на русском.
Фокусируйся на практике и результатах.
"""

SYSTEM_PROMPT_PLAN = """
Ты помощник по планированию тренировок Андрея Потапова.
Помогай структурировать планы недели, месяца, сезон.
Учитывай интенсивность, восстановление, специфику бега.
Отвечай кратко, с примерами конкретных тренировок.
"""

SYSTEM_PROMPT_CONTENT = """
Ты помощник по созданию контента для бега и AI-ботов.
Помогай писать посты, идеи контента, структурировать материал.
Фокусируйся на практичности, истории, мотивации.
Пиши в стиле Андрея Потапова: живо, с примерами, без воды.
"""

SYSTEM_PROMPT_AI_BOT = """
Ты помощник по AI-ботам и автоматизации контента.
Помогай с интеграцией OpenAI, Claude, создавать промпты.
Объясняй архитектуру, best practices, отладку.
Отвечай с примерами кода и конкретными решениями.
"""

# Max message history
MAX_HISTORY_LENGTH = 10  # Keep last 10 messages per user
