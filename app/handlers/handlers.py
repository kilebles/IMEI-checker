import re
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

  await message.answer("Привет, вы можете отправить IMEI на проверку и я верну информацию по нему.")
  

def is_valid_imei(imei: str) -> bool:
  return bool(re.fullmatch(r"\d{15}", imei))


@router.message()
async def imei_handler(message: Message):
  if message.text.startswith("/"):
    return
  
  imei = message.text.strip()
  if not is_valid_imei(imei):
    await message.answer("Пожалуйста, отправьте корректный IMEI")
    return
  
  await message.answer(f"Проверяю IMEI: {imei}.\nИнформация: <данные об устройстве>.")