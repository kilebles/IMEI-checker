import logging
import uvicorn
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from aiogram import Bot, Dispatcher
from aiogram.types import Update
from app.core.config import config
from app.commands.set_commands import set_commands
from app.handlers.handlers import router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

dp.include_router(router)

@asynccontextmanager
async def lifespan(app: FastAPI):
  logging.info("Starting app...")
  await bot.set_webhook(config.WEBHOOK_URL)
  await set_commands(bot)

  yield

  await bot.delete_webhook()
  await bot.session.close()

app = FastAPI(lifespan=lifespan)

@app.post(config.WEBHOOK_PATH)
async def process_webhook(request: Request):
  json_data = await request.json()
  update = Update(**json_data)
  await dp.feed_update(bot, update)
  return {"status": "ok"}

if __name__ == "__main__":
  uvicorn.run(
    app, 
    host=config.HOST, 
    port=config.PORT
  )