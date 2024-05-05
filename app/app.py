from typing import Tuple
from loguru import logger
from sys import stderr
from aiogram import Bot, Dispatcher

from app.config import Config, LogConfig
from app.container import init_container


async def create_app(config: Config) -> Tuple[Bot, Dispatcher]:
    init_logger(config.log)
    container = await init_container(config)

    dispatcher = container.dispatcher()
    bot = await container.bot()

    return bot, dispatcher


def init_logger(config: LogConfig) -> None:
    logger.remove()
    logger.add(stderr, level=config.LEVEL.upper())
    
    if config.DIR:
        logger.add(
            f'{config.DIR}/logs.log',
            compression='zip',
            rotation=f'{config.ROTATION} MB',
            retention=config.RETENTION,
            level=config.LEVEL.upper()
        )
