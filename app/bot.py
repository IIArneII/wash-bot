from loguru import logger
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.methods import GetUpdates, SendMessage

from app.config import BotConfig


async def middleware(make_request, bot: Bot, method: SendMessage):
    if type(method) not in [GetUpdates]:
        if type(method) is SendMessage:
            msg = method.text.replace('\n', ' ')
            logger.info(f"Send message. Chat id: {method.chat_id}. Message: {msg}")
        else:
            logger.info(f"Method: {type(method)}")
    
    return await make_request(bot, method)


async def init_bot(config: BotConfig) -> Bot:
    logger.info('Bot initialization...')
    
    config: BotConfig = config if type(config) is BotConfig else BotConfig(config)
    bot = Bot(config.TOKEN, parse_mode=ParseMode.HTML)
    bot.session.middleware(middleware)

    await bot.delete_webhook(drop_pending_updates=True)

    return bot


def init_dispatcher() -> Dispatcher:
    logger.info('Dispatcher initialization...')

    from app.transport.bot import base_router

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(base_router)
    return dp
