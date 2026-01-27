import os
import logging
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, F
from aiogram.types import Update, Message
from aiogram.client.session.aiohttp import AiohttpSession
from openai import OpenAI

from config import (
    TELEGRAM_BOT_TOKEN,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    SYSTEM_PROMPT_DEFAULT,
    SYSTEM_PROMPT_PLAN,
    SYSTEM_PROMPT_CONTENT,
    SYSTEM_PROMPT_AI_BOT,
    MAX_HISTORY_LENGTH
)
from services.openai_client import OpenAIService
from services.memory import MemoryService
from handlers.commands import router as command_router
from handlers.messages import router as message_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize services
openclient = OpenAI(api_key=OPENAI_API_KEY)
openai_service = OpenAIService(model=OPENAI_MODEL, client=openclient)
memory_service = MemoryService(max_history=MAX_HISTORY_LENGTH)

# Telegram setup
session = AiohttpSession()
bot = Bot(token=TELEGRAM_BOT_TOKEN, session=session)
dp = Dispatcher()

# Register routers
dp.include_router(command_router)
dp.include_router(message_router)

# FastAPI app
app = FastAPI()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Receive updates from Telegram."""
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return {"ok": False, "error": str(e)}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
