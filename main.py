import os
import logging

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.session.aiohttp import AiohttpSession

from config import TELEGRAM_BOT_TOKEN
from handlers.commands import router as commands_router
from handlers.messages import router as messages_router
from handlers import posts, qa

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

session = AiohttpSession()
bot = Bot(token=TELEGRAM_BOT_TOKEN, session=session)
dp = Dispatcher()

dp.include_router(commands_router)
dp.include_router(messages_router)
dp.include_router(posts.router)
dp.include_router(qa.router)

app = FastAPI()


@app.post("/webhook")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()
        update = Update.model_validate(data)
        await dp.feed_update(bot, update)
        return {"ok": True}
    except Exception:
        logger.exception("Webhook error")
        return {"ok": False}


@app.get("/health")
async def health():
    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
