import os
import sys

from loguru import logger


def load_env(env_name: str) -> str:
    env_var = os.getenv(env_name, default=None)
    if env_var is not None:
        return env_var
    raise ValueError(f"Environment variable {env_name} is undefined")


try:

    VK_BOT_KEY = load_env("VK_BOT_KEY")
    VK_GROUP_KEY = load_env("VK_GROUP_KEY")
    VK_GROUP_ID = int(load_env("VK_GROUP_ID"))
    VK_LIKES_REPORT_CHAT_ID = int(load_env("VK_LIKES_REPORT_CHAT_ID"))
except ValueError as error:
    logger.error("Ошибка чтения переменных окружения из .env-файла {}", error)
    sys.exit(1)
else:
    logger.success("Переменные окружения успешно прочитаны")
