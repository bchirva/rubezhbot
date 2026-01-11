import sys

from loguru import logger

LOG_FILE = "logs/rubezhbot.log"


def configure_log():

    logger.remove()
    logger.add(
        sys.stdout,
        format="{time:YYYY-MM-DD HH:mm:ss} <level>{level}:</level> {message}",
        level="DEBUG",
    )
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} {level}: {message}",
        rotation="100 Mb",
        retention="7 days",
        level="SUCCESS",
    )

    logger.success("Логгирование сконфигурированно")
