# Andrey Personal Assistant Bot

Личный Telegram AI-ассистент для Андрея Потапова. Помогает с генерацией контента о беге, отвечает на вопросы по базе знаний и помогает с AI-ботами.

## Основные функции

- **Генерация постов:** Команды `/post_easy`, `/post_beginner`, `/post_community`, `/post_about` для создания черновиков постов.
- **База знаний (Q&A):** Команда `/ask [вопрос]` для ответов на вопросы о беге, тренировках и сообществе.
- **AI-помощник:** Помощь с OpenAI, Claude и автоматизацией.
- **Память:** Бот помнит контекст последних 10 сообщений в обычном чате.

## Стек технологий

- **Python 3.10+**
- **Aiogram 3.x** (Telegram Bot Framework)
- **FastAPI** + **Uvicorn** (Web-сервер для Webhooks)
- **OpenAI API** (GPT-4o / GPT-4o-mini)

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/fox24x-hub/andrey-personal-assistant-bot.git
   cd andrey-personal-assistant-bot
   ```

2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

3. Создайте файл `.env` в корне проекта и добавьте переменные:
   ```env
   TELEGRAM_BOT_TOKEN=your_token
   OPENAI_API_KEY=your_key
   OPENAI_MODEL=gpt-4o-mini
   WEBHOOK_HOST=https://your-domain.com
   ```

4. Запустите бота:
   ```bash
   python main.py
   ```

## Развёртывание

Проект настроен для работы через Webhooks. На платформах вроде Railway или Render бот автоматически устанавливает webhook при запуске благодаря `lifespan` в `main.py`.
