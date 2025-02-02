import json
import re
import asyncio
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from app.core.config import config
from app.utils.API import check_imei

router = Router()

def is_valid_imei(imei: str) -> bool:
  return bool(re.fullmatch(r"\d{15}", imei))


@router.message(CommandStart())
async def cmd_start_handler(message: Message):
  if message.from_user.id not in config.WHITE_LIST:
    error_message = await message.answer("Извините, вы не в белом списке ❌")
    await asyncio.sleep(3)
    await error_message.delete()
    return

  await message.answer("Привет, вы можете отправить IMEI на проверку и я верну информацию по нему.")
  

@router.message()
async def imei_handler(message: Message):
  if message.from_user.id not in config.WHITE_LIST:
    return
  
  if message.text.startswith("/"):
    return
  
  imei = message.text.strip()
  if not is_valid_imei(imei):
    error_message = await message.answer("Пожалуйста, отправьте корректный IMEI ❌")
    await asyncio.sleep(3)
    await error_message.delete()
    return
  
  waiting_message = await message.answer("⏳")
  result_text = await check_imei(imei)
  
  await waiting_message.delete()
  await message.answer(result_text)