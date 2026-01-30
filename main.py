import os
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from aiogram.client.session.aiohttp import AiohttpSession

from config import TELEGRAM_BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PORT
from handlers.commands import router as commands_router
from handlers.messages import router as messages_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and dispatcher
session = AiohttpSession()
bot = Bot(token=TELEGRAM_BOT_TOKEN, session=session)
dp = Dispatcher()

# Include routers
dp.include_router(commands_router)
dp.include_router(messages_router)


def build_webhook_url() -> str | None:
    """Безопасная сборка URL вебхука."""
    host = (WEBHOOK_HOST or "").strip()
    if not host:
        logger.warning("WEBHOOK_HOST is empty, webhook will not be set")
        return None

    # убираем протокол, если случайно передали с https://
    host = host.replace("https://", "").replace("http://", "").strip("/")
    url = f"https://{host}/webhook"
    logger.info(f"Using webhook URL: {url}")
    return url


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_url = build_webhook_url()
    if webhook_url:
        try:
            await bot.set_webhook(url=webhook_url, drop_pending_updates=True)
            logger.info("✅ Webhook set successfully")
        except Exception as e:
            logger.exception(f"❌ Failed to set webhook: {e}")
    else:
        logger.info("Webhook is not configured (polling-only setup or local run)")

    try:
        yield
    finally:
        try:
            await bot.session.close()
        except Exception:
            pass


app = FastAPI(lifespan=lifespan)


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
    return {
        "status": "ok",
        "webhook_host": WEBHOOK_HOST,
    }


if __name__ == "__main__":
    import uvicorn

    port = int(os.getenv("PORT", WEBHOOK_PORT))
    logger.info(f"Starting app on 0.0.0.0:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
