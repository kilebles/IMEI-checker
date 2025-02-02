import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    HOST = os.getenv("APP_HOST", "0.0.0.0")
    PORT = int(os.getenv("APP_PORT", "8080"))
    WEBHOOK_HOST = os.getenv("WEBHOOK_HOST")
    WEBHOOK_PATH = os.getenv("WEBHOOK_PATH")
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"
    WHITE_LIST = list(map(int, os.getenv("ALLOWED_USER_IDS", "").split(",")))
    IMEI_CHECK_URL = os.getenv("IMEI_CHECK_URL")
    IMEI_CHECK_TOKEN = os.getenv("API_AUTH_TOKEN", "")
    SERVICE_ID = str(os.getenv("SERVICE_ID", "1"))


config = Config()
