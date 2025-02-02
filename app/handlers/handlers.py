from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.core.config import config

router = Router()

@router.message(CommandStart())
async def cmd_start_handler(message: Message):
  if message.from_user.id not in config.WHITE_LIST:
    await message.answer("Извините, вы не в белом списке.")
    return

  await message.answer("Привет! Ты в белом списке")